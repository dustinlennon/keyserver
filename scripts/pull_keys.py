
import requests
import logging
from logging.handlers import RotatingFileHandler
import sys
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--keyfile", default = "ubuntu_key_cert")
parser.add_argument("--output")
parser.add_argument("--logfile", default = "logs/pull_keys.log")
parser.add_argument("--console", action = "store_true")


logger = logging.getLogger(__name__)

#--- set_logger ---------------------------------------------------------------
def set_logger(logfile, console = False):

  # Ensure the log location.  On failure, log to console.
  try:
    p = Path(logfile).absolute()
    p.parent.mkdir(exist_ok = True)
  except (PermissionError,) as e:
    console = True

  formatter_args = {
    'style' : '{',
    'datefmt' : "%Y-%m-%d %H:%M:%S",
    'fmt' : "[{asctime}] {levelname:<8} {message}"
  }

  formatter = logging.Formatter(**formatter_args)

  if console:
    handler = logging.StreamHandler(sys.stderr)
  else:
    handler = RotatingFileHandler(logfile, maxBytes = 32000, backupCount=3)

  handler.setFormatter(formatter)
  logger.addHandler(handler)
  logger.setLevel(logging.INFO)

#--- write_content ------------------------------------------------------------
def write_content(output, content):
  try:
    with open(output, "w") as f:
      logger.info(f"writing to {output}")
      f.write(content)
  except (PermissionError,) as e:    
    errmsg = str(e)
    logger.error(errmsg)
    raise e
     
#--- main ---------------------------------------------------------------------
if __name__ == '__main__':

  args = parser.parse_args()
  set_logger(args.logfile, args.console)

  url = f"http://192.168.1.104:8022/{args.keyfile}"
  output = args.output or f"/home/ubuntu/.ssh/authorized_keys"

  try:
    r = requests.get(url)
    msg = f"HTTP/{r.status_code} : {url}"
    r.raise_for_status()
    content = r.content.decode("utf8")

  except (requests.exceptions.HTTPError,) as e:    
    logger.error(msg)

  else:    
    logger.info(msg)
    write_content(output, content)

     
