FROM hiroara/datascience-docker:python3

MAINTAINER Hiroki Arai <hiroara62@gmail.com>

RUN pip install git+https://github.com/hiroara/remotefile-python@v0.0.6

VOLUME /tmp/scripts
VOLUME /tmp/log

Add run_script.sh /tmp/scripts/run_script.sh

ENTRYPOINT ["/tmp/scripts/run_script.sh"]
