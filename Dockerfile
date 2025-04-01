# Use ./setup.sh script to build image

FROM python:3.12.3-alpine
RUN apk add git

ENV APP_PATH=/home/keyserver
RUN mkdir -p $APP_PATH

WORKDIR $APP_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ENV PYTHONPATH=$APP_PATH

ADD archive.tgz $APP_PATH
