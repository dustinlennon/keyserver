import sys

from pathlib import Path

from scaffold.params.base_params import BaseParams
from scaffold.params.mixins import *

import requests
import requests.exceptions

# --- KsRequestParams ---------------------------------------------------------

class KsRequestParams(BaseParams, LoggerInitializerMixin):
  _prefix = "KSREQUEST"

  def assign_params(self, conf, args):
    super().assign_params(conf, args)

    u = conf.main.url
    self.url = f"{u.scheme}://{u.netloc}/{u.path}"

# --- main --------------------------------------------------------------------

if __name__ == '__main__':

  params  = KsRequestParams.build()
  logger  = params.get_logger("keyserver.ksrequest")

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

  logger.info("acquired authorized_keys")
  print(content.decode("utf8"))

