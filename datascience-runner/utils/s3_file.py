from utils.remote_file import RemoteFile

import os
import re
import logging

import boto.s3 as s3
from boto.utils import get_instance_metadata
from boto.s3.connection import OrdinaryCallingFormat

class S3File(RemoteFile):
    def __init__(self, url, cache_dir='/tmp/s3', region_name=None):
        self.url = url
        self.region_name = self.get_region_name(region_name)
        self.cache_dir = cache_dir
        self.local_path = self.get_local_path()

    def get_local_path(self):
        return os.path.join(self.cache_dir, self.url.scheme, self.region_name, self.url.netloc, re.sub('^/', '', self.url.path))


    def download(self):
        with open(self.local_path, 'wb') as f:
            self.__get_s3_object().get_contents_to_file(f, cb=lambda current, total: logging.info('Downloading {} ({:d}/{:d})'.format(self.local_path, current, total)))
        logging.info('Downloading {} has been completed.'.format(self.local_path))
        return self.local_path

    def get_region_name(self, region_name):
        if region_name == None: region_name = self.__get_region_name()
        if region_name == None: raise Exception('Region name is required! Please use region option (--region <region name>).')
        return region_name

    def __get_s3_instance(self):
        return s3.connect_to_region(self.region_name, calling_format=OrdinaryCallingFormat())

    def __get_s3_object(self):
        return self.__get_s3_instance().get_bucket(self.url.netloc).get_key(self.url.path)

    def __get_region_name(self):
        return get_instance_metadata(timeout=3, num_retries=1)
