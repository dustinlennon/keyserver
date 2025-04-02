#!/bin/bash

sshkey_path=/home/dnlennon/.ssh/keys/mrdl

pubkeys=(mrdl_ca.pub mrdl_ubuntu.pub)
destdirs=(/opt/keyserver /home/dnlennon/Workspace/Sandbox/keyserver-service)

for dd in ${destdirs[@]}; do
	mkdir -p $dd/keys
	for pk in ${pubkeys[@]}; do
		cp -f $sshkey_path/$pk $dd/keys/$pk
	done
done

