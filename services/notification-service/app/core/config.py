from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str = "development"

    database_url: str            = "postgresql+asyncpg://cipher:cipher_pass@postgres:5432/cipher_db"
    kafka_bootstrap_servers: str = "kafka:29092"

    github_app_id: str               = ""
    github_app_private_key_path: str = "/secrets/github-app.pem"

    sendgrid_api_key: str = ""
    frontend_url: str     = "http://localhost:3000"

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"

settings = Settings()
