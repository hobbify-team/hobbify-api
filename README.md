# Hobbify API

A habits tracker for nerds.

## Commands

<!-- Build the images -->
docker-compose -f local.yml build

<!-- Run the stack -->
docker-compose -f local.yml up

export COMPOSE_FILE=local.yml

docker-compose build
docker-compose up
docker-compose ps
docker-compose down

<!-- Admin commands -->
docker-compose run --rm django COMMAND

E.g.

docker-compose run --rm django python manage.py createsuperuser


## Enable debugger
Run Django in a different session in order to interact with it.

docker-compose up
docker-compose ps
docker rm -f <ID>

docker-compose run --rm --service-ports django
