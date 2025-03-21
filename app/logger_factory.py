import sys
from pathlib import Path

import logging
from logging.handlers import RotatingFileHandler

class LoggerFactory(object):
  _formatter = None
  _handlers = {}

  @classmethod
  def formatter(cls):
    if cls._formatter:
      return cls._formatter
    
    formatter_args = {
      'style' : '{',
      'datefmt' : "%Y-%m-%d %H:%M:%S",
      'fmt' : "[{asctime}] {levelname:<8} {message}"
    }
    cls._formatter = logging.Formatter(**formatter_args)

  @classmethod
  def handler(cls, logfile):
    handler = cls._handlers.get(logfile)
    if handler:
      return handler

    try:
      p = Path(logfile).absolute()
      p.parent.mkdir(exist_ok = True)
    except (PermissionError,) as e:
      handler = logging.StreamHandler(sys.stderr)
    else:
      handler = RotatingFileHandler(logfile, maxBytes = 1e7, backupCount=3)

    handler.setFormatter(cls._formatter)

    cls._handlers[logfile] = handler
    return handler

  @classmethod
  def acquire(cls, name, logfile, level = logging.INFO):
    logger = logging.getLogger(name)
    handler = cls.handler(logfile)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger
