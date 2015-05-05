import logging

import boto.s3 as s3
from boto.utils import get_instance_metadata
from urllib.parse import urlparse
from boto.s3.connection import OrdinaryCallingFormat
import os
import re

class RemoteFile:
    def __init__(self, path, region_name=None, output_dir=None):
        self.url = urlparse(path)
        self.region_name = self.get_region_name(region_name)
        self.output_dir = output_dir if output_dir != None else '/tmp/data'

    def get_region_name(self, region_name):
        if region_name == None: region_name = self.__get_region_name()
        if region_name == None: raise Exception('Region name is required! Please use region option (--region <region name>).')
        return region_name

    def __get_s3_instance(self):
        return s3.connect_to_region(self.region_name, calling_format=OrdinaryCallingFormat())

    def __get_s3_object(self):
        return self.__get_s3_instance().get_bucket(self.url.netloc).get_key(self.url.path)

    def __get_s3_file(self):
        file_path = self.get_local_path()
        if os.path.isfile(file_path):
            return file_path
        else:
            return self.__download_s3_file()

    def __download_s3_file(self):
        file_path = self.get_local_path()
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        logging.info('Start to download {}.'.format(file_path))
        with open(file_path, 'wb') as f:
            self.__get_s3_object().get_contents_to_file(f, cb=lambda current, total: logging.info('Downloading {} ({:d}/{:d})'.format(file_path, current, total)))
        logging.info('Downloading {} has been completed.'.format(file_path))
        return file_path

    def get_local_path(self):
        return os.path.join(self.output_dir, 's3', self.region_name, self.url.netloc, re.sub('^/', '', self.url.path))

    def get_file_path(self):
        if self.is_s3_file():
            return self.__get_s3_file()
        else:
            return self.url.path

    def enable(self):
        if self.is_s3_file():
            self.__get_s3_file()

    def open(self):
        return open(self.get_file_path(), 'rb')

    def read(self):
        with self.open() as f:
            return f.read()

    def is_s3_file(self):
        return self.url.scheme == 's3'

    def __get_region_name(self):
        return get_instance_metadata(timeout=3, num_retries=1)
