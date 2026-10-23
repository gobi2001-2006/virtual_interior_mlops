.PHONY: help install test test-backend test-frontend dev backend frontend db-migrate db-seed docker-up docker-down

help:
	@echo "Available commands:"
	@echo "  make install        - Install all backend and frontend dependencies"
	@echo "  make dev            - Run backend and frontend concurrently"
	@echo "  make backend        - Run FastAPI backend server"
	@echo "  make frontend       - Run Vite React frontend dev server"
	@echo "  make test           - Run all backend and frontend tests"
	@echo "  make test-backend   - Run pytest suite"
	@echo "  make test-frontend  - Run frontend test suite"
	@echo "  make db-migrate     - Run Alembic database migrations"
	@echo "  make db-seed        - Seed furniture catalog into database"
	@echo "  make docker-up      - Start full stack in Docker Compose"
	@echo "  make docker-down    - Stop Docker Compose stack"

install:
	python -m pip install -r backend/requirements.txt
	cd frontend && npm install

backend:
	python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

frontend:
	cd frontend && npm run dev

test: test-backend test-frontend

test-backend:
	python -m pytest backend/tests ml/tests -v

test-frontend:
	cd frontend && npm test

db-migrate:
	alembic upgrade head

db-seed:
	python -m backend.app.db.init_db

docker-up:
	docker compose up -d --build

docker-down:
	docker compose down
