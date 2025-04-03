#!/bin/bash

# enable script by creating symbolic link: .git/hooks/post-commit

>&2 echo ">>> running post-commit script"
>&2 echo ">>> GIT_DIR:       ${GIT_DIR}"
>&2 echo ">>> GIT_WORK_TREE: ${GIT_WORK_TREE}"

keyserver_path=/opt/keyserver
install_path=/home/dnlennon/Workspace/Sandbox/keyserver-service

if [ ! -d "$keyserver_path" ]; then
	sudo mkdir -p "$keyserver_path"	
	sudo chown root:adm "$keyserver_path"
	sudo chmod 2775 "$keyserver_path"

	mkdir -p "$keyserver_path/assets"
	mkdir -p "$keyserver_path/conf"
	mkdir -p "$keyserver_path/keys"

	ln ${PWD}/freshen-keys.sh "$keyserver_path"
fi

# Copy the public keys
>&2 echo ">>> copying public keys"
${PWD}/freshen-keys.sh

# Initialize the assets
>&2 echo ">>> initializing assets"
pipenv run python scripts/kscreate.py

# Create hard links to conf
>&2 echo ">>> creating hard links"
find "${install_path}/conf" -type f | xargs -I% ln -f % ${keyserver_path}/conf


