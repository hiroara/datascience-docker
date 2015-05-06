from utils.remote_file import RemoteFile

import logging
import os
import re
import urllib.request as request

class HTTPFile(RemoteFile):
    def __init__(self, url, cache_dir='/tmp/http', region_name=None):
        self.url = url
        self.cache_dir = cache_dir
        self.local_path = self.get_local_path()

    def get_local_path(self):
        return os.path.join(self.cache_dir, self.url.scheme, self.url.netloc, re.sub('^/', '', self.url.path))

    def download(self):
        request.urlretrieve(self.url.geturl(), self.local_path, lambda blocknum, blocksize, totalsize: logging.info('Downloading {} ({:d}/{:d})'.format(self.local_path, blocknum * blocksize, totalsize)))
        logging.info('Downloading {} has been completed.'.format(self.local_path))
        return self.local_path
