from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str = "development"

    database_url: str        = "postgresql+asyncpg://cipher:cipher_pass@postgres:5432/cipher_db"
    redis_url: str           = "redis://redis:6379/0"
    kafka_bootstrap_servers: str = "kafka:29092"

    inference_service_url: str = "http://inference-service:8000"
    s3_bucket_logs: str        = "cipher-logs-dev"
    aws_region: str            = "ap-south-1"

    github_app_id: str               = ""
    github_app_private_key_path: str = "/secrets/github-app.pem"

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"

settings = Settings()
