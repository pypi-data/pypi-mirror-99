FROM python:3.6

ARG nb2workflow_revision
RUN git clone https://github.com/volodymyrss/nb2workflow.git /nb2workflow; cd /nb2workflow; git reset --hard $nb2workflow_revision; pip install -r requirements.txt; pip install .[docker,service,rdf,cwl,numpy]; rm -rf /nb2workflow

RUN useradd -ms /bin/bash oda

RUN pip install git+https://github.com/volodymyrss/flask-caching.git@control_with_response#egg=flask-caching

USER oda
WORKDIR /workdir


ENTRYPOINT cp -rfv /repo/* .; [ -s /deploy-env ] && . /deploy-env; nb2service /repo/ --host 0.0.0.0 --port 5000
