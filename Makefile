.PHONY: setup dev web api test lint build docker-up docker-down

setup:
	npm install
	python3 -m venv .venv
	.venv/bin/pip install -e "apps/api[dev]"

dev:
	docker compose up --build

web:
	npm run dev

api:
	.venv/bin/uvicorn app.main:app --app-dir apps/api --reload

test:
	npm test
	.venv/bin/pytest apps/api

lint:
	npm run lint
	npm run typecheck
	.venv/bin/ruff check apps/api

build:
	npm run build

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down
