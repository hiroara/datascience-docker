FROM hiroara/datascience-docker:python3

MAINTAINER Hiroki Arai <hiroara62@gmail.com>

RUN pip install awscli boto

Add run_script.py /tmp/run_script.py

ENTRYPOINT ["/tmp/run_script.py"]
