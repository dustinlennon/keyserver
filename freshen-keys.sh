#!/bin/bash

keyserver_path=/opt/keyserver
install_path=/home/dnlennon/Workspace/Sandbox/keyserver-service

find -L "$install_path/keys" -type f \
	| xargs -I% realpath % \
	| xargs -I% ln -f % ${keyserver_path}/keys
