
Run Locally
====


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

```bash
SCAFFOLD_IMAGE_NAME=keyserver ./build_image.sh

# site
KEYSERVER_PATH=$PWD docker compose -f docker-compose.yaml up site

# create
KEYSERVER_PATH=$PWD docker compose -f docker-compose.yaml run --rm create

# request
KEYSERVER_PATH=$PWD docker compose -f docker-compose.yaml run --rm request

```