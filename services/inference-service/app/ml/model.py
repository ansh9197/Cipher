import logging
import os
import mlflow
from mlflow.tracking import MlflowClient
from app.core.config import settings
from typing import Optional, Any

logger = logging.getLogger(__name__)

_model = None
_model_version = None


def load_model() -> Optional[Any]:
    """
    Try to load the production model from MLflow registry.
    Falls back to rule-based mode if no model is registered yet.
    """
    global _model, _model_version

    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
    client = MlflowClient()

    try:
        versions = client.get_latest_versions(
            settings.model_name,
            stages=[settings.model_stage]
        )
        if not versions:
            logger.warning(f"No '{settings.model_stage}' model found in MLflow — using rule-based fallback")
            return None

        latest = versions[0]
        _model_version = latest.version
        logger.info(f"Loading model {settings.model_name} v{_model_version} from MLflow")

        model_uri = f"models:/{settings.model_name}/{settings.model_stage}"
        _model = mlflow.pyfunc.load_model(model_uri)
        logger.info("Model loaded successfully")
        return _model

    except Exception as e:
        logger.warning(f"Could not load model from MLflow ({e}) — using rule-based fallback")
        return None


def get_model():
    return _model


def get_model_version():
    return _model_version
