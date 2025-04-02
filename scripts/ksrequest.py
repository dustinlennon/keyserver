import sys

from pathlib import Path

from scaffold.params.base_params import BaseParams
from scaffold.params.mixins import *

import requests
import requests.exceptions

if __name__ == '__main__':

  class KsRequestParams(BaseParams, NowMixin, LoggerInitMixin):
    _prefix = "KSREQUEST"

    def assign_args(self, conf, args):
      super().assign_args(conf, args)
      self.keys_path    = str(args.keys_path)

      u = conf.ksrequest.url
      self.url = f"{u.scheme}://{u.netloc}/{u.path}"

  params  = KsRequestParams.build()
  logger  = params.get_logger(__name__)

  # Create output directory
  pth = Path(params.keys_path)
  pth.mkdir(parents = True, exist_ok = True)
  pth.chmod(0o700)

  # Make HTTP request   
  try:
    r : requests.Response = requests.get(params.url, timeout = 1)
    r.raise_for_status()

  except requests.exceptions.HTTPError as e:
    msg = f"HTTP/{r.status_code} : {params.url}"
    logger.info(msg)
    sys.exit(0)

  except requests.exceptions.RequestException as e:    
    logger.error(str(e))
    sys.exit(1)
  
  else:
    content = r.content

  # Output the file
  try:
    pk = pth / f"{u.path}.pub"
    with open(pk, "wb") as f:
      f.write(content)
    logger.info(f"wrote {pk}")

  except (FileNotFoundError, PermissionError) as e:
    logger.error(str(e))
    logger.error(msg)
    sys.exit(1)

