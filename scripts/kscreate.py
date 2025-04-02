from scaffold.params.base_params import BaseParams
from scaffold.params.mixins import *

# --- KsCreateParams ----------------------------------------------------------

class CommonParams(NowMixin, LoggerInitializerMixin, JinjaTemplateMixin):
  pass

class KsCreateParams(BaseParams, CommonParams):
  _prefix = "KSCREATE"

  def assign_params(self, conf, args):
    super().assign_params(conf, args)
    self.keys_path    = str(args.keys_path)
    self.assets_path  = args.assets_path
    self.pk_map       = conf.main.pk_map


# --- main --------------------------------------------------------------------

if __name__ == '__main__':

  params  = KsCreateParams.build()
  logger  = params.get_logger(__name__)

  # public key metadata
  pk_map = {
    pkid : f"{params.keys_path}/{keyfile}"
    for pkid, keyfile in vars(params.pk_map).items()
  }

  pub_keys = {}
  for key_id,key_file in pk_map.items():
    with open(key_file) as f:
      pub_keys[key_id] = f.read().strip()

  # 'ca' is a special case
  ca = pub_keys.pop('ca')

  # retrieve the template
  updated_at = params.now()
  template = params.get_template("authorized_keys.j2")
  shared_args = {
    'updated_at' : updated_at,
    'cert' : ca
  }

  # loop over the user and create assets
  for user,key in pub_keys.items():
    rendering = template.render(
      **shared_args,
      user = user,
      key = key,
      include_cert = False
    )

    filename = f"{params.assets_path}/{user}_key"
    with open(filename, "w") as f:
      f.write(rendering)
      logger.info(f"writing {filename}")

    rendering = template.render(
      **shared_args,
      user = user,
      key = key,
      include_cert = True
    )
    filename = f"{params.assets_path}/{user}_key_cert"
    with open(filename, "w") as f:
      f.write(rendering)
      logger.info(f"writing {filename}")
