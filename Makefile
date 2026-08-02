.PHONY: up down build backend frontend test

up:
	docker compose up --build

down:
	docker compose down

build:
	docker compose build

backend:
	docker compose up backend

frontend:
	docker compose up frontend

test:
	docker compose run --rm backend pytest
