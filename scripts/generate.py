from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from datetime import datetime

from shared import get_config

env = Environment(
  loader = FileSystemLoader("./templates")
)

if __name__ == '__main__':

  keys = {}
  config = get_config()
  ssh_path = Path(config.ssh_path)

  updated_at = datetime.now().isoformat()

  # read the 'ca' and 'ubuntu' public keys
  p = ssh_path / f"{config.net_name}_ca.pub"
  with open(p) as f:
    keys['ca'] = f.read().strip()

  p = ssh_path / f"{config.net_name}_ubuntu.pub"
  with open(p) as f:
    keys['ubuntu'] = f.read().strip()

  template = env.get_template("authorized_keys.j2")
  shared_args = {
    'updated_at' : updated_at,
    'keys' : keys
  }

  # ubuntu account, key only
  rendering = template.render(
    **shared_args,
    include_cert = False
  )
  with open("./www/html/ubuntu_key", "w") as f:
     f.write(rendering)


  # ubuntu account, key + CA
  template = env.get_template("authorized_keys.j2")
  rendering = template.render(
    **shared_args,
    include_cert = True
  )
  with open("./www/html/ubuntu_key_cert", "w") as f:
     f.write(rendering)
