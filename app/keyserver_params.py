import os
from app.base_params import BaseParams

import argparse
class KeyserverParams(BaseParams):
  _prefix = "KEYSERVER"

  def __init__(self, *, cfg, **kws):
    super().__init__(cfg = cfg)
    self.net_name = cfg.net_name


