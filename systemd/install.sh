#!/usr/bin/bash
# systemctl enable ./keyserver.service ./keyserver-watcher.path ./keyserver-watcher.service
# systemctl start keyserver.service
sudo systemctl enable \
	./kssite.service \
	./kscreate.service \
	./kscreate-watcher.path \
	./ksrequest.service \
	./ksrequest.timer
