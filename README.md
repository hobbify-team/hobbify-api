# Hobbify API

This project is based on the Sub-routine project proposed to C2 as final project.

Hobbify is a habits tracker system, what does that mean? Well, you can create a habit and give it a frequency, a start and end date, and start updating it to track your process all over the habit.

## How to run the stack

To run the stack you need docker installed in your system and follow the next steps:

1. Clone this repository `git clone [git@github.com](mailto:git@github.com):hobbify-team/hobbify-api.git`.
2. Move to the root of the folder and build the docker images with the next command: `docker-compose -f local.yml build`.
3. Then run the stack with: `docker-compose -f local.yml up`.

## Enable debugger
Run Django in a different session in order to interact with it.

docker-compose up
docker-compose ps
docker rm -f <ID>

docker-compose run --rm --service-ports django

## Code quality
Check all posible erros with flake8 with the next command:

`docker-compose run --rm --service-ports django python -m flake8`
