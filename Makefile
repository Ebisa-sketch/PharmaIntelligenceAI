.PHONY: help install-backend install-frontend run-backend run-frontend test-backend test-frontend docker-up docker-down

help:
	@echo "PharmaIntelligence AI - Makefile Commands"
	@echo "-----------------------------------------"
	@echo "make install-backend   - Install backend Python dependencies"
	@echo "make install-frontend  - Install frontend Node dependencies"
	@echo "make run-backend       - Run FastAPI backend development server"
	@echo "make run-frontend      - Run Next.js frontend development server"
	@echo "make test-backend      - Run backend pytest suites"
	@echo "make test-frontend     - Run frontend tests"
	@echo "make docker-up         - Start Docker Compose services"
	@echo "make docker-down       - Stop Docker Compose services"

install-backend:
	cd backend && pip install -r requirements.txt

install-frontend:
	cd frontend && npm install

run-backend:
	cd backend && uvicorn app.main:app --reload --port 8000

run-frontend:
	cd frontend && npm run dev

test-backend:
	cd backend && pytest

test-frontend:
	cd frontend && npm test

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

