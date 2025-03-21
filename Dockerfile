FROM python:3.12-alpine3.21

ENV APP_PATH=/home/keyserver

RUN mkdir -p $APP_PATH

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
ENV PYTHONPATH=$APP_PATH

WORKDIR $APP_PATH

ENV KEYSERVER_PATH=$APP_PATH

# COPY scripts ${HDIR}/scripts
# VOLUME ${HDIR}/
# ENTRYPOINT ["/usr/local/bin/python", "/home/notify/app/notify.py"]
