COMPOSE_FILE=docker-compose.yml

create-requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

migrate:
	alembic upgrade head

build-image:
	docker-compose -f $(COMPOSE_FILE) build

up: build-image
	docker-compose -f $(COMPOSE_FILE) up -d

	