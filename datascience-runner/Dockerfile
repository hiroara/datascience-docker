FROM hiroara/datascience-docker:python3

MAINTAINER Hiroki Arai <hiroara62@gmail.com>

RUN pip install awscli boto

Add run_script.py /tmp/scripts/run_script.py
Add utils /tmp/scripts/utils

ENTRYPOINT ["/tmp/scripts/run_script.py"]
