import sys

from scaffold.params.base_params import BaseParams
from scaffold.params.mixins import *
from scaffold.debug import TraceClassDecorator

from http import HTTPStatus
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

import logging

# --- KsSiteParams ------------------------------------------------------------

class KsSiteParams(BaseParams, LoggerInitializerMixin):
  _prefix = "KSSITE"

  def assign_params(self, conf, args):
    super().assign_params(conf, args)
    self.assets_path    = str(args.assets_path)
    self.port           = conf.main.port
    self.bind_addr      = conf.main.bind_addr

# --- FileRequestHandler ------------------------------------------------------

class FileRequestHandler(SimpleHTTPRequestHandler):
  logger = logging.getLogger("keyserver.kssite")

  def list_directory(self, path):
    self.send_error(
      HTTPStatus.FORBIDDEN,
      "No permission to list directory"
    )
    return None
  
  def fmt_message(self, format, *args):
    message = format % args
    message = "%s - %s" % (
      self.address_string(),
      message.translate(self._control_char_table)
    )
    return message

  def log_message(self, format, *args):
    msg = self.fmt_message(format, *args)
    self.logger.info(msg)

  def log_error(self, format, *args):
    msg = self.fmt_message(format, *args)
    self.logger.error(msg)

# --- main --------------------------------------------------------------------

if __name__ == '__main__':
  
  params = KsSiteParams.build()

  class FileServer(ThreadingHTTPServer):
    def finish_request(self, request, client_address):
      self.RequestHandlerClass(request, client_address, self, directory = params.assets_path)

  httpd = FileServer(
    (params.bind_addr, params.port),
    FileRequestHandler
  )

  try:
      httpd.serve_forever()
  except KeyboardInterrupt:
      print("\nKeyboard interrupt received, exiting.")
      sys.exit(0)
