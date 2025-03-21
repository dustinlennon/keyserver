#!/bin/bash

KEYSERVER_PATH=$PWD

docker run -it --rm \
	-v ${KEYSERVER_PATH}/app:/home/keyserver/app \
	-v ${KEYSERVER_PATH}/aux:/home/keyserver/aux \
	keyserver:latest \
	/bin/sh
