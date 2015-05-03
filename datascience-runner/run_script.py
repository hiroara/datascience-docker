#!/usr/bin/env python

import boto.s3 as s3
from boto.utils import get_instance_metadata
from urllib.parse import urlparse
from boto.s3.connection import OrdinaryCallingFormat
import os
import re

class RemoteFile:
    def __init__(self, path, region_name=None, output_dir=None):
        self.url = urlparse(path)
        self.region_name = region_name
        self.output_dir = output_dir if output_dir != None else '/tmp'

    def get_s3_instance(self):
        if region_name == None: self.region_name = get_region_name()
        if region_name == None: raise Exception('Region name is required! Please use region option (--region <region name>).')
        return s3.connect_to_region(region_name, calling_format=OrdinaryCallingFormat())

    def get_s3_object(self):
        return self.get_s3_instance().get_bucket(self.url.netloc).get_key(self.url.path)

    def get_s3_file(self):
        file_path = os.path.join(self.output_dir, 's3', self.region_name, self.url.netloc, re.sub('^/', '', self.url.path))
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        self.get_s3_object().get_contents_to_file(open(file_path, 'wb'))
        return file_path

    def get_file(self):
        if self.is_s3_file():
            return open(self.get_s3_file(), 'rb')
        else:
            return open(url.path, 'rb')

    def get_file_content(self):
        with self.get_file() as f:
            return f.read()

    def is_s3_file(self):
        return self.url.scheme == 's3'

    def get_region_name():
        return get_instance_metadata(timeout=3, num_retries=1)

class Runner(RemoteFile):
    def exec_script(self):
        exec(compile(self.get_file_content(), self.url.path, 'exec'), {}, {})


if __name__ == '__main__':
    from argparse import ArgumentParser

    usage = 'Usage: python {} script [--region <region name>] [--help]'.format(__file__)
    argparser = ArgumentParser(usage=usage)
    argparser.add_argument('script', type=str, help='Path for Python script (available in S3|local)')
    argparser.add_argument('-r', '--region', help='AWS Region')
    args = argparser.parse_args()

    region_name = args.region if args.region else None

    runner = Runner(args.script, region_name=region_name)
    runner.exec_script()
