import sys

from scaffold.params.base_params import BaseParams
from scaffold.params.mixins import *

from http import HTTPStatus
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

class KsSiteHttpRequestHandler(SimpleHTTPRequestHandler):
  def list_directory(self, path):
    self.send_error(
      HTTPStatus.FORBIDDEN,
      "No permission to list directory"
    )
    return None

if __name__ == '__main__':

  class KsSiteParams(BaseParams, LoggerInitMixin):
    _prefix = "KSSITE"

    def assign_args(self, conf, args):
      super().assign_args(conf, args)
      self.assets_path    = str(args.assets_path)
      self.port           = conf.main.port
      self.bind_addr      = conf.main.bind_addr

  params = KsSiteParams.build()

  class FileServer(ThreadingHTTPServer):
    def finish_request(self, request, client_address):
      self.RequestHandlerClass(request, client_address, self, directory = params.assets_path)
 
  httpd = FileServer(
    (params.bind_addr, params.port),
    KsSiteHttpRequestHandler
  )

  try:
      httpd.serve_forever()
  except KeyboardInterrupt:
      print("\nKeyboard interrupt received, exiting.")
      sys.exit(0)
