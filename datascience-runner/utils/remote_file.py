from urllib.parse import urlparse
import os
import sys
import logging

class RemoteFile:
    def __init__(self, path, *args, **kwargs):
        self.url = urlparse(path)

        if self.is_s3_file():
            from utils.s3_file import S3File
            self.remote = S3File(self.url, *args, **kwargs)
        elif self.is_http_file():
            from utils.http_file import HTTPFile
            self.remote = HTTPFile(self.url, *args, **kwargs)

        if self.is_local_file():
            self.local_path = self.url.path
        else:
            self.local_path = self.remote.local_path

    def download(self):
        self.mkdir_p()
        logging.info('Start to download {}.'.format(self.local_path))
        return self.remote.download()

    def get_file_path(self, force=False):
        if self.is_local_file(): return self.local_path
        if not force and os.path.isfile(self.local_path): return self.local_path

        return self.download()

    def enable(self, **kwargs):
        self.get_file_path(**kwargs)

    def open(self, **kwargs):
        return open(self.get_file_path(**kwargs), 'rb')

    def read(self, force=False):
        with self.open(force=force) as f: return f.read()

    def is_s3_file(self):
        return self.url.scheme == 's3'

    def is_http_file(self):
        return self.url.scheme == 'http'

    def is_local_file(self):
        return not self.is_s3_file() and not self.is_http_file()

    def mkdir_p(self):
        os.makedirs(os.path.dirname(self.local_path), exist_ok=True)


class Runner(RemoteFile):
    def exec_script(self, *args):
        self.enable(force=True)
        cmd = self.__build_command(args)
        logging.info('Now invoking `{}`.'.format(cmd))
        exitcode = os.system(cmd)
        if exitcode == 0:
            logging.info('Command `{}` has been successfully completed.'.format(cmd))
        else:
            logging.info('Command `{}` has been completed with error code {}.'.format(cmd, exitcode))
            sys.exit(exitcode)

    def __build_command(self, args):
        return '/usr/bin/env python {} {}'.format(self.local_path, self.__build_args(args))

    def __build_args(self, args):
        return ' '.join(['{}'.format(arg) for arg in args])
