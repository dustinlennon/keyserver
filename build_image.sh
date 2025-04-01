#!/usr/bin/bash

LOGS_PATH=${SCAFFOLD_LOGS_PATH:-/var/log/scaffold}
IMAGE_NAME=keyserver

archive=(scripts templates)

if [ ! -d "$LOGS_PATH" ]; then
	>&2 echo "Creating log directory: $LOGS_PATH"
	sudo mkdir -p "$LOGS_PATH"
	sudo chown root:adm "$LOGS_PATH"
	sudo chmod 02750 "$LOGS_PATH"
fi

if [ ! -h "./scaffold-logs" ]; then
	>&2 echo "Creating symbolic link: ./scaffold-logs"
	ln -s "$LOGS_PATH" ./scaffold-logs
fi

>&2 echo "Creating archive.tgz"
tar \
	--exclude='*/__pycache__/*' \
	-czf archive.tgz ${archive[@]}

>&2 echo "Creating requirements.txt"
pipenv requirements > requirements.txt

>&2 echo "Building image: $KEYSERVER"
docker build \
	--tag $KEYSERVER:latest \
	.
