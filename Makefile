.PHONY: help dev-up dev-down dev-logs build test migrate fresh infra-up

help:
	@echo ""
	@echo "  make dev-up       start all services"
	@echo "  make dev-down     stop all services"
	@echo "  make dev-logs     tail all logs"
	@echo "  make build        rebuild all images"
	@echo "  make migrate      run DB migrations"
	@echo "  make fresh        wipe volumes and restart"
	@echo "  make infra-up     start only postgres+redis+kafka"
	@echo ""

dev-up:
	docker compose up -d
	@echo "Waiting 20s for services to start..."
	@sleep 20
	@echo "Auth service:         http://localhost:8001/health"
	@echo "Webhook service:      http://localhost:8002/health"
	@echo "Analysis service:     http://localhost:8003/health"
	@echo "Inference service:    http://localhost:8004/health"
	@echo "Notification service: http://localhost:8005/health"
	@echo "Frontend:             http://localhost:3000"
	@echo "MLflow:               http://localhost:5000"

dev-down:
	docker compose down

dev-logs:
	docker compose logs -f

build:
	docker compose build --parallel

migrate:
	docker compose exec auth-service alembic upgrade head

fresh:
	docker compose down -v
	docker compose up -d --build

infra-up:
	docker compose up -d postgres redis zookeeper kafka mlflow
	@echo "Infrastructure ready"

test-auth:
	@echo "Testing auth service..."
	curl -s http://localhost:8001/health | python3 -m json.tool
	@echo ""
	curl -s -X POST http://localhost:8001/api/v1/auth/register \
	  -H "Content-Type: application/json" \
	  -d '{"email":"dev@cipher.dev","password":"Test1234!","full_name":"Dev User"}' \
	  | python3 -m json.tool
