from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str = "development"

    database_url: str = "postgresql+asyncpg://cipher:cipher_pass@postgres:5432/cipher_db"
    kafka_bootstrap_servers: str = "kafka:29092"

    github_webhook_secret: str = "dev-secret"

    # Plan limits — how many analyses per month per plan
    plan_limits: dict = {
        "free":       50,
        "starter":    500,
        "pro":        -1,   # unlimited
        "enterprise": -1,
    }

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"

settings = Settings()
