
Run Locally
====

N.B., logging will be in ./logs/keyserver.log

```bash
#site
pipenv run python3 scripts/kssite.py 

# create
pipenv run python3 scripts/kscreate.py 

# request
pipenv run python3 scripts/ksrequest.py 
```


Run Dockerized
====

N.B., logging will be in /var/log/scaffold/keyserver.log

```bash
# Refresh /opt/keyserver
SCAFFOLD_IMAGE_NAME=keyserver ./build_image.sh && ./post-commit.sh

# Serve assets:
docker compose -f /opt/keyserver/conf/compose.yaml up site

# Create assets:
docker compose -f /opt/keyserver/conf/compose.yaml run --rm create

# Request assets:
docker compose -f /opt/keyserver/conf/compose.yaml run --rm request

```


Systemd
====


```bash
# enable the unit files:
sudo systemctl enable \
	./kssite.service \
	./kscreate.service \
	./kscreate-watcher.path

# (re)start the services
sudo systemctl restart kssite.service 
sudo systemctl restart kscreate-watcher.path

# cleanup / reset
sudo systemctl daemon-reload 
sudo systemctl reset-failed 
```