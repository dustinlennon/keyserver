#!/usr/bin/bash
sudo systemctl enable ./keyserver.service
sudo systemctl add-requires keyserver.service ./keyserver-watcher.path ./keyserver-watcher.service
