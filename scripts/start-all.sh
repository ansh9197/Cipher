#!/bin/bash
set -e
cd ~/cipher

echo "=== CIPHER Startup ==="

echo "[1/6] Starting infrastructure..."
docker compose up -d postgres redis zookeeper
sleep 25

echo "[2/6] Checking postgres..."
until docker exec cipher-postgres pg_isready -U cipher 2>/dev/null; do
  echo "  waiting for postgres..."
  sleep 5
done
echo "  postgres ready"

echo "[3/6] Starting Kafka..."
docker compose up -d kafka
sleep 15

echo "[4/6] Starting MLflow..."
docker compose up -d mlflow
sleep 20

echo "[5/6] Starting all services..."
docker compose up -d \
  auth-service \
  webhook-service \
  analysis-service \
  inference-service \
  notification-service \
  frontend
sleep 20

echo "[6/6] Health checks..."
for port in 8001 8002 8003 8004 8005 3000 5000; do
  result=$(curl -s --max-time 4 http://localhost:$port/health 2>/dev/null || \
           curl -s --max-time 4 http://localhost:$port/ 2>/dev/null | head -c 30)
  if [ -z "$result" ]; then
    echo "  Port $port: FAILED"
  else
    echo "  Port $port: OK"
  fi
done

echo ""
echo "Done. Visit http://$(curl -s https://checkip.amazonaws.com):3000"
