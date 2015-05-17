#!/bin/sh

mkdir -p /tmp/log
remote-runner "$@" 2>&1 | tee -a /tmp/log/python.log
