#!/bin/bash

# enable script by creating symbolic link: .git/hooks/post-commit

>&2 echo ">>> running post-commit script"
>&2 echo ">>> GIT_DIR:       ${GIT_DIR}"
>&2 echo ">>> GIT_WORK_TREE: ${GIT_WORK_TREE}"

# sudo cp -rp . /opt/keyserver-service
