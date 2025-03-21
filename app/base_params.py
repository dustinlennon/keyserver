import os
import datetime, pytz
from types import SimpleNamespace
from typing import Optional

import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader

from app.dotenv_reader import DotenvReader

#- get_config -----------------------------------------------------------------

def get_config(config_path):
  with open(config_path) as f:
    config = yaml.load(f, Loader=Loader)
    if config is not None:
      config = _preprocess(config)
  return config

def _preprocess(d):
  obj = d
  if isinstance(d, list):
    dx = []
    for o in d:
      dx.append( _preprocess(o) )
    obj = dx
  elif isinstance(d, dict):
    dx = {}
    for k,v in d.items():
      dx[k] = _preprocess(v)
    obj = SimpleNamespace(**dx)

  return obj

#- BaseParams -----------------------------------------------------------------

class BaseParams(object):
  _prefix : str 
  _opt_path : Optional[str]

  def __init__(self, *, cfg):
    cwd = os.getcwd()
    self._path = os.environ.get(f"{self._prefix}_PATH", cfg.env.path or f"{cwd}")

    timezone  = os.environ.get(f"{self._prefix}_TIMEZONE", cfg.env.timezone)
    self._tz  = pytz.timezone(timezone)

  @classmethod
  def from_path(cls, config_path):
    instance = cls(
      cfg = get_config(config_path)
    )
    return instance
  
  @classmethod
  def from_dotenv(cls):
    result = DotenvReader([
      cls._opt_path,
      'dotenv'
    ]).read()

    base_path = result.get(f"{cls._prefix}_PATH")
    config_path = os.path.sep.join(
      [p for p in [base_path, "aux", "config.yaml"] if p]
    )

    instance = cls.from_path(config_path)
    return instance

  def app_path(self, *args):
    pth = os.path.sep.join([self._path, "app"] + list(args))
    return pth

  def aux_path(self, *args):
    pth = os.path.sep.join([self._path, "aux"] + list(args))
    return pth

  def now(self):
    return datetime.datetime.now(self._tz)

