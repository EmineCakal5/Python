all: up

up:
	docker-compose up -d --build

down:
	docker-compose down

build:
	docker-compose build

re: down up

.PHONY: all up down build re
