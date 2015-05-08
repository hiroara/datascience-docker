#!/bin/sh

mkdir -p /tmp/log
/usr/bin/env python $(dirname $0)/run_script.py "$@" 2>&1 | tee -a /tmp/log/python.log
