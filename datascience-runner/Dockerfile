FROM hiroara/datascience-docker:python3

MAINTAINER Hiroki Arai <hiroara62@gmail.com>

RUN pip install git+https://github.com/hiroara/remotefile-python@v0.0.12

VOLUME /tmp/scripts
VOLUME /tmp/log

Add run_script.sh /tmp/scripts/run_script.sh
Add install_pkgs.sh /tmp/scripts/install_pkgs.sh

ENTRYPOINT ["/tmp/scripts/run_script.sh"]
