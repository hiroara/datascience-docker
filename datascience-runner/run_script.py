#!/usr/bin/env python

import boto.s3 as s3
from boto.utils import get_instance_metadata
from urllib.parse import urlparse
from boto.s3.connection import OrdinaryCallingFormat

def exec_script(content, filename):
    exec(compile(content, filename, 'exec'), {}, {})

def get_script(url, region_name=None):
    if url.scheme == 's3':
        s3 = get_s3_instance(region_name)
        return s3.get_bucket(url.netloc).get_key(url.path).get_contents_as_string()
    else:
        return open(url.path, 'rb').read()

def get_s3_instance(region_name=None):
    if region_name == None: region_name = get_region_name()
    if region_name == None: raise Exception('Region name is required! Please use region option (--region <region name>).')
    return s3.connect_to_region(region_name, calling_format=OrdinaryCallingFormat())

def get_region_name():
    get_instance_metadata(timeout=3, num_retries=1)

if __name__ == '__main__':
    from argparse import ArgumentParser

    usage = 'Usage: python {} script [--region <region name>] [--help]'.format(__file__)
    argparser = ArgumentParser(usage=usage)
    argparser.add_argument('script', type=str, help='Path for Python script (available in S3|local)')
    argparser.add_argument('-r', '--region', help='AWS Region')
    args = argparser.parse_args()

    region_name = args.region if args.region else None

    url = urlparse(args.script)
    script = get_script(url, region_name=region_name)
    exec_script(script, url.path)
