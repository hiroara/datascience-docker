#!/bin/sh

if [ ! -z "$PIP_PKGS" ]; then
  echo $PIP_PKGS
  echo $PIP_PKGS | $(dirname $0)/install_pkgs.sh
fi
mkdir -p /tmp/log
remote-runner "$@" 2>&1 | tee -a /tmp/log/python.log
