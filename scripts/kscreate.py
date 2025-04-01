from scaffold.params.base_params import BaseParams
from scaffold.params.mixins import *
from scaffold.debug import TraceClassDecorator

if __name__ == '__main__':

  class CommonParams(NowMixin, LoggerInitMixin, JinjaTemplateMixin):
    pass

  @TraceClassDecorator(mro = True)
  class KeyserverParams(BaseParams, CommonParams):
    _prefix = "KSCREATE"

    def assign_args(self, args):
      super().assign_args(args)
      self.keys_path    = args.keys_path
      self.assets_path  = args.assets_path

  params  = KeyserverParams.build()
  logger  = params.get_logger(__name__)

  # public key metadata
  pk_map = {
    pkid : f"{params.keys_path}/{keyfile}"
    for pkid, keyfile in vars(params.aux.pk_map).items()
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
