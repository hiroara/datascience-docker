#!/usr/bin/env python

from utils import Runner

if __name__ == '__main__':
    import logging
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    from argparse import ArgumentParser

    usage = 'Usage: python {} script [--region <region name>] [--help]'.format(__file__)
    argparser = ArgumentParser(usage=usage)
    argparser.add_argument('script', type=str, help='Path for Python script (available in S3|local)')
    argparser.add_argument('-r', '--region', help='AWS Region')
    args = argparser.parse_args()

    region_name = args.region if args.region else None

    runner = Runner(args.script, cache_dir='/tmp/src', region_name=region_name)
    runner.exec_script()
