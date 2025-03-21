import os
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from datetime import datetime

from app.keyserver_params import KeyserverParams

if __name__ == '__main__':

  # Instantiate a KeyserverParams object
  keyserver_path = os.environ.get("KEYSERVER_PATH")
  if keyserver_path: 
    config_file = f"{keyserver_path}/aux/config.yaml"
    params = KeyserverParams.from_path(config_file)
  else:
    params = KeyserverParams.from_dotenv()


  key_path = Path(params.aux_path("keys"))
  updated_at = params.now().isoformat()

  # create the jinja2 environment
  env = Environment(
    loader = FileSystemLoader(
      params.app_path("templates")
    )
  )

  # 
  #
  # DOES THIS EVEN NEED TO RUN IN DOCKER?
  #
  #

  # public key metadata
  pk_meta = {
    'ca'      : f"{params.net_name}_ca.pub",
    'ubuntu'  : f"{params.net_name}_ubuntu.pub"
  }

  pub_keys = {}
  for key_id,key_file in pk_meta.items():
    p = key_path / key_file
    with open(p) as f:
      pub_keys[key_id] = f.read().strip()

  # 'ca' is a special case
  ca = pub_keys.pop('ca')

  # retrieve the template
  template = env.get_template("authorized_keys.j2")
  shared_args = {
    'updated_at' : updated_at,
    'ca' : ca
  }

  # loop over the user and create assets
  for user,key in pub_keys.items():
    rendering = template.render(
      **shared_args,
      user = user,
      key = key,
      include_cert = False
    )

    filename = params.aux_path(f"/assets/{user}_key")
    with open(filename, "w") as f:
      f.write(rendering)

    rendering = template.render(
      **shared_args,
      user = user,
      key = key,
      include_cert = True
    )
    filename = params.aux_path(f"./assets/{user}_key_cert")
    with open(filename, "w") as f:
      f.write(rendering)
