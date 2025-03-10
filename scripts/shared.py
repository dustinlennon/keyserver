from types import SimpleNamespace

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def get_config():
  with open("config.yaml") as f:
    config = load(f, Loader=Loader)
    config = SimpleNamespace(**config)
  return config
