#!/bin/bash
# Run retraining manually at any time
cd ~/cipher

MLFLOW_IP=$(docker inspect cipher-mlflow \
  --format='{{range $k,$v := .NetworkSettings.Networks}}{{$v.IPAddress}}{{end}}')
POSTGRES_IP=$(docker inspect cipher-postgres \
  --format='{{range $k,$v := .NetworkSettings.Networks}}{{$v.IPAddress}}{{end}}')

echo "Running retraining job..."
echo "MLflow: $MLFLOW_IP | Postgres: $POSTGRES_IP"

docker run --rm \
  --network cipher-network \
  -e MLFLOW_TRACKING_URI=http://${MLFLOW_IP}:5000 \
  -e DATABASE_URL=postgresql://cipher:cipher_pass@${POSTGRES_IP}:5432/cipher_db \
  -e MIN_SAMPLES=10 \
  -e GIT_PYTHON_REFRESH=quiet \
  cipher/retraining-job:latest

echo "Retraining complete. Check MLflow at http://localhost:5000"
