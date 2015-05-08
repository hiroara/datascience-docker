FROM hiroara/datascience-docker:python3

MAINTAINER Hiroki Arai <hiroara62@gmail.com>

RUN pip install awscli boto
ENV PYTHONPATH /tmp/scripts

Add run_script.py /tmp/scripts/run_script.py
Add run_script.sh /tmp/scripts/run_script.sh
Add utils /tmp/scripts/utils

ENTRYPOINT ["/tmp/scripts/run_script.sh"]
