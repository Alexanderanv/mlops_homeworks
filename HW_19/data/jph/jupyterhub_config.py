import os
from typing import Any
import dockerspawner
from traitlets.config.application import get_config

c: Any = get_config()

c.JupyterHub.hub_ip = "0.0.0.0"
c.JupyterHub.hub_port = 8010
c.JupyterHub.hub_connect_ip = "jph"

c.JupyterHub.cookie_secret_file = "/data/jupyterhub_cookie_secret"
c.JupyterHub.db_url = "sqlite:////data/jupyterhub.sqlite"
c.ConfigurableHTTPProxy.pid_file = "/data/jupyterhub-proxy.pid"

c.JupyterHub.admin_users = [os.environ["JPH_ADMIN_USER"]]
c.JupyterHub.authenticator_class = "dummy"
c.DummyAuthenticator.password = os.environ["JPH_DUMMY_PASSWORD"]

c.JupyterHub.spawner_class = dockerspawner.DockerSpawner

c.DockerSpawner.image = os.getenv("DOCKER_NOTEBOOK_IMAGE", "jupyterhub/singleuser")
c.DockerSpawner.cmd = os.getenv("DOCKER_SPAWNER_CMD", "start-singleuser.sh")

notebook_dir = os.getenv("DOCKER_NOTEBOOK_DIR", "/home/jovyan")
c.DockerSpawner.notebook_dir = notebook_dir
c.DockerSpawner.volumes = {"jupyter-user-{username}": notebook_dir}
c.DockerSpawner.environment = {
 "JPH_SINGLEUSER_JPHCONTENTS_ROOTDIR": notebook_dir,
}

c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = os.environ["DOCKER_NETWORK_NAME"]

c.DockerSpawner.remove = True
c.DockerSpawner.debug = True