#!/usr/bin/bash

sudo systemctl daemon-reload 
sudo systemctl reset-failed 
sudo systemctl restart kssite.service 
sudo systemctl restart kscreate-watcher.path
# sudo systemctl status kssite.service 

