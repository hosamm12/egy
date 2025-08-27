SHELL := /bin/bash

up:
	docker compose --env-file .env up -d --build

down:
	docker compose --env-file .env down

logs:
	docker compose --env-file .env logs -f --tail=200

ps:
	docker compose --env-file .env ps
