#!/bin/bash

sshkey_path=/home/dnlennon/.ssh/keys/mrdl

pubkeys=(mrdl_ca.pub mrdl_ubuntu.pub)

for pk in ${pubkeys[@]}; do
	cp -f $sshkey_path/$pk /opt/keyserver/keys/$pk
done
