#!/usr/bin/bash
systemctl enable ./keyserver.service ./keyserver-watcher.path ./keyserver-watcher.service
systemctl start keyserver.service
