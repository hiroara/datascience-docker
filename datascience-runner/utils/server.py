from utils.remote_file import RemoteFile

import logging
from socketserver import TCPServer

class Server(RemoteFile):
    def serve_forever(self, *args, port=80):
        self.enable(force=True)
        from importlib.machinery import SourceFileLoader
        handler = SourceFileLoader('handler', self.local_path).load_module()
        Handler = handler.get_handler(*args)
        server = TCPServer(('0.0.0.0', port), Handler)
        logging.info('Serving at port {:d} with handler: {}'.format(port, Handler))
        server.serve_forever()
