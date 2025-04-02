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
	ln ${PWD}/freshen-keys.sh "$keyserver_path"
fi

dirs=(assets conf keys)
for d in ${dirs[@]}; do
	mkdir -p "${keyserver_path}/$d"
	find -L "$install_path/$d" -type f | xargs -I% realpath % | xargs -I% ln -f % ${keyserver_path}/${d}
done
