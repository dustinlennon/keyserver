#!/usr/bin/bash

tar czf archive.tgz scripts conf templates
pipenv requirements > requirements.txt

docker build \
	--tag keyserver-service:latest \
	.
