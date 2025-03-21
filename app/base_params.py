from types import SimpleNamespace
from typing import Optional

from abc import ABC

import os
import re
import datetime, pytz
import argparse

import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader

from app.dotenv_reader import DotenvReader
from app.exception_throwing_parser import ExceptionThrowingParser, ParserFallbackException

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

class BaseParams(ABC):
  _prefix : str 
  _opt_path : Optional[str] = None

  def __init__(self, cfg):
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help = "a yaml config file")

    for name, default_value in vars(cfg.env).items():
      full_name   = f"{self._prefix}_{name}"

      env_name    = self.env_name(full_name)
      attr_name   = self.attr_name(name)
      param_name  = self.param_name(name)

      value = os.environ.get(env_name, default_value)
      setattr(self, attr_name, value)

      parser.add_argument(
        f"--{param_name}",
        default = getattr(self, attr_name),
        help=f"{env_name}"
      )

    self.parser = parser

  @staticmethod
  def env_name(s):
    s = re.sub("-", "_", s)
    s = re.sub("[^_A-Za-z0-9]", "", s)
    return s.upper()

  @staticmethod
  def attr_name(s):
    s = re.sub("-", "_", s)
    s = re.sub("[^_A-Za-z0-9]", "", s)
    return s.lower()
  
  @staticmethod
  def param_name(s):
    s = re.sub("_", "-", s)
    s = re.sub("[^-A-Za-z0-9]", "", s)
    return s.lower()

  def parse_args(self):
    args = self.parser.parse_args()
    print(args)

  @classmethod
  def from_path(cls, config_path):
    cfg = get_config(config_path)

    instance = cls(cfg)
    return instance

  @classmethod
  def build(cls):
    instance = None

    try:
      print("trying from_env()")
      instance = cls.from_env()
    except KeyError:
      pass
    else:
      return instance

    try:
      print("trying from_args()")
      instance = cls.from_args(Parser = ExceptionThrowingParser)
    except ParserFallbackException as e:
      exit_args = (e.parser, 2, str(e))
    else:
      return instance

    try:
      print("trying from_dotenv()")
      instance = cls.from_dotenv()
    except Exception as e:
      argparse.ArgumentParser.exit(*exit_args)

    return instance

  @classmethod
  def from_env(cls):
    env_name = f"{cls._prefix}_CONFIG_PATH"
    config = os.environ[env_name]
    instance = cls.from_path(config)
    return instance

  @classmethod
  def from_args(cls, Parser = argparse.ArgumentParser):
    parser = Parser()
    parser.add_argument("--config", required = True, help = "a yaml config file")

    args, _ = parser.parse_known_args()
    instance = cls.from_path(args.config)

    return instance

  @classmethod
  def from_dotenv(cls):
    locs = [ p for p in 
      [
        cls._opt_path,
        'dotenv'
      ] if p
    ]

    result = DotenvReader(locs).read()
    config_file = result.get(f"{cls._prefix}_CONFIG_PATH")

    instance = cls.from_path(config_file)
    return instance

  def now(self):
    self._tz  = pytz.timezone(self.timezone)
    return datetime.datetime.now(self._tz)

if __name__ == '__main__':

  class KeyserverParams(BaseParams):
    _prefix = "KEYSERVER"

  params = KeyserverParams.build()
  params.parse_args()
