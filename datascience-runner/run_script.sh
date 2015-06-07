#!/bin/sh

if [ ! -z "$PIP_PKGS" ]; then
  echo $PIP_PKGS | $(dirname $0)/install_pkgs.sh
fi
if [ $# -gt 0 ]; then
  remote-runner "$@"
else
  python
fi
