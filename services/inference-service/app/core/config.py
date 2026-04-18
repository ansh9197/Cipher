from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str = "development"

    mlflow_tracking_uri: str = "http://mlflow:5000"
    model_name: str          = "cipher-classifier"
    model_stage: str         = "Production"

    aws_region: str    = "ap-south-1"
    s3_bucket_models: str = "cipher-models-dev"

    # Categories the model classifies into
    failure_categories: list = [
        "test_failure",
        "dependency_error",
        "build_error",
        "timeout",
        "auth_failure",
        "infra_error",
        "unknown",
    ]

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"

settings = Settings()
