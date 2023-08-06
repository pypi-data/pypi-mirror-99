import mlflow.models
import mlflow.models.docker_utils
import mlflow.sagemaker.cli

import mlflow.pyfunc as pyfunc
import mlflow.pyfunc.scoring_server as ss

import mlflow.models.container as mlflowcontainer
from mlflow.models.docker_utils import DISABLE_ENV_CREATION
from mlflow.version import VERSION as MLFLOW_VERSION
from pkg_resources import resource_filename

import signal
import multiprocessing
import os
import shutil
from subprocess import check_call, Popen

from mlflow.models import Model
from mlflow.models.model import MLMODEL_FILE_NAME

from lariat.version import __version__ as LARIAT_VERSION

_PyFuncModel = pyfunc.PyFuncModel
_scoring_server_init = ss.init


def _make_lariat_log(message, tags):
    ddtags = ",".join([f"{k}:{v}" for k, v in tags.items()])
    logs_dct = {
        "ddsource": "agent",
        "ddtags": ddtags,
        "hostname": "yes",
        "message": message,
    }
    return logs_dct


def _log_lariat(messages):
    import requests

    DD_API_KEY = "788a2c583db787d3485e46e99fda3dff"
    headers = {"Content-type": "application/json", "DD-API-KEY": DD_API_KEY}
    return requests.post(
        "https://http-intake.logs.datadoghq.com/v1/input",
        json=messages,
        headers=headers,
    )


def _patched_install_pyfunc_deps(model_path=None, install_mlflow=False):
    """
    Creates a conda env for serving the model at the specified path and installs almost all serving
    dependencies into the environment - MLflow is not installed as it's not available via conda.
    """
    # If model is a pyfunc model, create its conda env (even if it also has mleap flavor)
    has_env = False
    if model_path:
        model_config_path = os.path.join(model_path, MLMODEL_FILE_NAME)
        model = Model.load(model_config_path)
        # NOTE: this differs from _serve cause we always activate the env even if you're serving
        # an mleap model
        if pyfunc.FLAVOR_NAME not in model.flavors:
            return
        conf = model.flavors[pyfunc.FLAVOR_NAME]
        if pyfunc.ENV in conf:
            print("creating and activating custom environment")
            env = conf[pyfunc.ENV]
            env_path_dst = os.path.join("/opt/mlflow/", env)
            env_path_dst_dir = os.path.dirname(env_path_dst)
            if not os.path.exists(env_path_dst_dir):
                os.makedirs(env_path_dst_dir)
            shutil.copyfile(os.path.join(mlflowcontainer.MODEL_PATH, env), env_path_dst)
            conda_create_model_env = "conda env create -n custom_env -f {}".format(
                env_path_dst
            )
            if Popen(["bash", "-c", conda_create_model_env]).wait() != 0:
                raise Exception("Failed to create model environment.")
            has_env = True
    activate_cmd = ["source /miniconda/bin/activate custom_env"] if has_env else []
    # NB: install gunicorn[gevent] from pip rather than from conda because gunicorn is already
    # dependency of mlflow on pip and we expect mlflow to be part of the environment.
    install_server_deps = [
        "pip install gunicorn[gevent] requests lariat-run==" + LARIAT_VERSION
    ]
    if (
        Popen(["bash", "-c", " && ".join(activate_cmd + install_server_deps)]).wait()
        != 0
    ):
        raise Exception(
            "Failed to install serving dependencies into the model environment."
        )
    if has_env and install_mlflow:
        install_mlflow_cmd = [
            "pip install /opt/mlflow/."
            if mlflowcontainer._container_includes_mlflow_source()
            else "pip install mlflow=={}".format(MLFLOW_VERSION)
        ]
        if (
            Popen(["bash", "-c", " && ".join(activate_cmd + install_mlflow_cmd)]).wait()
            != 0
        ):
            raise Exception("Failed to install mlflow into the model environment.")


def _patched_serve_pyfunc(model):
    conf = model.flavors[pyfunc.FLAVOR_NAME]
    bash_cmds = []
    if pyfunc.ENV in conf:
        if not os.environ.get(DISABLE_ENV_CREATION) == "true":
            _patched_install_pyfunc_deps(
                mlflowcontainer.MODEL_PATH, install_mlflow=True
            )
        bash_cmds += ["source /miniconda/bin/activate custom_env"]
    nginx_conf = resource_filename(
        mlflow.models.__name__, "container/scoring_server/nginx.conf"
    )

    # option to disable manually nginx. The default behavior is to enable nginx.
    start_nginx = (
        False
        if os.getenv(mlflowcontainer.DISABLE_NGINX, "false").lower() == "true"
        else True
    )
    nginx = Popen(["nginx", "-c", nginx_conf]) if start_nginx else None

    # link the log streams to stdout/err so they will be logged to the container logs.
    # Default behavior is to do the redirection unless explicitly specified by environment variable.

    if start_nginx:
        check_call(["ln", "-sf", "/dev/stdout", "/var/log/nginx/access.log"])
        check_call(["ln", "-sf", "/dev/stderr", "/var/log/nginx/error.log"])

    cpu_count = multiprocessing.cpu_count()
    os.system("pip -V")
    os.system("python -V")
    os.system('python -c"from mlflow.version import VERSION as V; print(V)"')
    cmd = (
        "LARIAT_GEVENT_PATCH_ALL=1 lariat-run gunicorn --log-level debug -w {cpu_count} ".format(
            cpu_count=cpu_count
        )
        + "${GUNICORN_CMD_ARGS} mlflow.models.container.scoring_server.wsgi:app"
    )
    bash_cmds.append(cmd)
    gunicorn = Popen(["/bin/bash", "-c", " && ".join(bash_cmds)])

    procs = [p for p in [nginx, gunicorn] if p]

    signal.signal(
        signal.SIGTERM, lambda a, b: _sigterm_handler(pids=[p.pid for p in procs])
    )
    # If either subprocess exits, so do we.
    awaited_pids = mlflowcontainer._await_subprocess_exit_any(procs=procs)
    _sigterm_handler(awaited_pids)


def _patched_build_and_push_container(build, push, container, mlflow_home):
    if not (build or push):
        print("skipping both build and push, have nothing to do!")
    if build:
        sagemaker_image_entrypoint = """
        ENTRYPOINT ["python", "-c", "import lariat.patch.mlflow as patch_mlflow; patch_mlflow.patch(); import sys; from mlflow.models import container as C; \
        C._init(sys.argv[1])"]
        """

        def setup_container(_):
            return "\n".join(
                [
                    'ENV {disable_env}="false"',
                    "RUN pip install lariat-run==" + LARIAT_VERSION,
                    'RUN python -c "import lariat.patch.mlflow as patch_mlflow;'
                    "patch_mlflow.patch();"
                    "from mlflow.models.container import _install_pyfunc_deps;"
                    '_install_pyfunc_deps(None, False)"',
                ]
            )

        mlflow.models.docker_utils._build_image(
            container,
            mlflow_home=os.path.abspath(mlflow_home) if mlflow_home else None,
            entrypoint=sagemaker_image_entrypoint,
            custom_setup_steps_hook=setup_container,
        )
    if push:
        mlflow.sagemaker.push_image_to_ecr(container)


class PatchedPyFuncModel(_PyFuncModel):
    def predict(self, data):
        schema = self.metadata.get_input_schema()
        cols = schema.column_names()
        base_tags = {
            "run_id": self.metadata.run_id,
            "artifact_path": self.metadata.artifact_path,
            "flavor": self.metadata.flavors[pyfunc.FLAVOR_NAME]["loader_module"],
        }

        result = super(PatchedPyFuncModel, self).predict(data)
        messages = []

        for i, row in data.iterrows():
            tags = dict(base_tags)
            tags["result"] = result[i]

            for col in cols:
                tags[col] = row[col]

            message = "input: " + str(row) + " output: " + str(result[i])
            messages.append(_make_lariat_log(message, tags))

        _log_lariat(messages)
        return result


class SagemakerLoggingMiddleware(object):
    def __init__(self, app):
        self._app = app

    def __call__(self, env, resp):
        def log_response(status_code, headers):
            r = resp(status_code, headers)
            _log_datadog(_make_datadog_log("yo", dict(r.headers)))
            return r

        return self._app(env, log_response)


def _patched_scoring_server_init(model):
    app = _scoring_server_init(model)
    # set the flask app to log interesting headers to requests
    app.wsgi_app = SagemakerLogger(app.wsgi_app)
    return app


def patch():
    pyfunc.PyFuncModel = PatchedPyFuncModel
    ss.init = _patched_scoring_server_init
    mlflowcontainer._install_pyfunc_deps = _patched_install_pyfunc_deps
    mlflowcontainer._serve_pyfunc = _patched_serve_pyfunc
    mlflow.sagemaker.cli.commands.commands[
        "build-and-push-container"
    ].callback = _patched_build_and_push_container
