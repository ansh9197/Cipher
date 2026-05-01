FROM ghcr.io/mlflow/mlflow:v2.9.2

RUN pip install --no-cache-dir psycopg2-binary==2.9.9

EXPOSE 5000

CMD ["mlflow", "server", \
     "--backend-store-uri", "postgresql://cipher:cipher_pass@postgres:5432/cipher_db", \
     "--default-artifact-root", "/mlflow/artifacts", \
     "--host", "0.0.0.0", \
     "--port", "5000"]
