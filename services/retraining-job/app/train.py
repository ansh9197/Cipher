"""
CIPHER Retraining Job
Runs every Sunday at 2am via Kubernetes CronJob.
Pipeline:
  1. Load labeled feedback from PostgreSQL
  2. Combine with existing training data from S3
  3. Fine-tune DistilBERT classifier
  4. Evaluate against held-out test set
  5. If F1 improves > 2% — promote to Production in MLflow
  6. Inference service hot-reloads new model automatically
"""

import os
import json
import logging
import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from mlflow.tracking import MlflowClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

# ── Config ────────────────────────────────────────────────────────────────────
MLFLOW_URI    = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
DATABASE_URL  = os.getenv("DATABASE_URL", "postgresql://cipher:cipher_pass@postgres:5432/cipher_db")
MODEL_NAME    = os.getenv("MODEL_NAME", "cipher-classifier")
MIN_SAMPLES   = int(os.getenv("MIN_SAMPLES", "50"))
MIN_F1_DELTA  = float(os.getenv("MIN_F1_DELTA", "0.02"))

CATEGORIES = [
    "test_failure",
    "dependency_error",
    "build_error",
    "timeout",
    "auth_failure",
    "infra_error",
    "unknown",
]

# ── Seed training data ────────────────────────────────────────────────────────
# These are hand-crafted examples that bootstrap the model
# before enough real feedback is collected
SEED_DATA = [
    {"text": "ModuleNotFoundError: No module named requests", "label": "dependency_error"},
    {"text": "npm ERR! missing: react@18.0.0", "label": "dependency_error"},
    {"text": "ImportError: cannot import name FastAPI", "label": "dependency_error"},
    {"text": "Cannot find module express", "label": "dependency_error"},
    {"text": "pip install failed: no matching distribution", "label": "dependency_error"},
    {"text": "FAILED tests/test_auth.py::test_login AssertionError", "label": "test_failure"},
    {"text": "pytest 5 failed 2 passed", "label": "test_failure"},
    {"text": "FAIL src/components/App.test.js", "label": "test_failure"},
    {"text": "Expected 200 but got 404", "label": "test_failure"},
    {"text": "AssertionError: assert response.status_code == 200", "label": "test_failure"},
    {"text": "SyntaxError: invalid syntax line 42", "label": "build_error"},
    {"text": "error TS2345: Argument of type string not assignable", "label": "build_error"},
    {"text": "compilation failed: exit code 1", "label": "build_error"},
    {"text": "ERROR in src/index.js Module not found", "label": "build_error"},
    {"text": "gcc error: undefined reference to main", "label": "build_error"},
    {"text": "Process completed with exit code 1 timeout exceeded", "label": "timeout"},
    {"text": "Job exceeded maximum time limit of 360 minutes", "label": "timeout"},
    {"text": "DeadlineExceeded: context deadline exceeded", "label": "timeout"},
    {"text": "Step timed out after 30 minutes", "label": "timeout"},
    {"text": "Permission denied: unable to access credentials", "label": "auth_failure"},
    {"text": "Error 403 Forbidden: authentication failed", "label": "auth_failure"},
    {"text": "InvalidClientTokenId: security token invalid", "label": "auth_failure"},
    {"text": "GITHUB_TOKEN expired or invalid", "label": "auth_failure"},
    {"text": "Connection refused: dial tcp 127.0.0.1:5432", "label": "infra_error"},
    {"text": "ECONNREFUSED: connection to database failed", "label": "infra_error"},
    {"text": "no such host: redis-service", "label": "infra_error"},
    {"text": "Failed to connect to kafka:9092", "label": "infra_error"},
    {"text": "network timeout connecting to external service", "label": "infra_error"},
]


def load_feedback_from_db() -> pd.DataFrame:
    """Load engineer-rated feedback from PostgreSQL."""
    try:
        # Use sync engine for the job
        sync_url = DATABASE_URL.replace("+asyncpg", "")
        engine = create_engine(sync_url)
        with engine.connect() as conn:
            # Check if feedback table exists
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_name = 'analysis_feedback'
                )
            """))
            exists = result.scalar()

            if not exists:
                logger.info("No feedback table yet — using seed data only")
                return pd.DataFrame(columns=["text", "label"])

            # Load positive feedback (rating = 1 means analysis was correct)
            rows = conn.execute(text("""
                SELECT log_text, predicted_category as label
                FROM analysis_feedback
                WHERE rating = 1
                  AND predicted_category IS NOT NULL
                  AND log_text IS NOT NULL
                  AND LENGTH(log_text) > 20
                ORDER BY created_at DESC
                LIMIT 5000
            """))
            df = pd.DataFrame(rows.fetchall(), columns=["text", "label"])
            logger.info(f"Loaded {len(df)} feedback examples from database")
            return df
    except Exception as e:
        logger.warning(f"Could not load feedback from DB: {e}")
        return pd.DataFrame(columns=["text", "label"])


def build_training_data(feedback_df: pd.DataFrame) -> pd.DataFrame:
    """Combine seed data with real feedback."""
    seed_df = pd.DataFrame(SEED_DATA)

    if len(feedback_df) > 0:
        combined = pd.concat([seed_df, feedback_df], ignore_index=True)
        logger.info(f"Combined: {len(seed_df)} seed + {len(feedback_df)} feedback = {len(combined)} total")
    else:
        combined = seed_df
        logger.info(f"Using seed data only: {len(combined)} examples")

    # Filter to known categories
    combined = combined[combined["label"].isin(CATEGORIES)]
    combined = combined.dropna(subset=["text", "label"])
    combined = combined.drop_duplicates(subset=["text"])

    logger.info(f"Final training set: {len(combined)} examples")
    logger.info(f"Category distribution:\n{combined['label'].value_counts()}")
    return combined


def get_current_production_f1() -> float:
    """Get F1 score of currently deployed production model."""
    try:
        mlflow.set_tracking_uri(MLFLOW_URI)
        client = MlflowClient()
        versions = client.get_latest_versions(MODEL_NAME, stages=["Production"])
        if not versions:
            logger.info("No production model exists yet — will promote new model automatically")
            return 0.0
        run_id = versions[0].run_id
        run = client.get_run(run_id)
        f1 = float(run.data.metrics.get("f1_weighted", 0.0))
        logger.info(f"Current production model F1: {f1:.4f}")
        return f1
    except Exception as e:
        logger.warning(f"Could not get production F1: {e}")
        return 0.0


def train_model(df: pd.DataFrame) -> tuple:
    """
    Train a TF-IDF + Logistic Regression classifier.
    This is Stage 2 of the AI pipeline — fast to train, good accuracy.
    When you have 1000+ examples, swap this for DistilBERT fine-tuning.
    """
    X = df["text"].tolist()
    y = df["label"].tolist()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y if len(set(y)) > 1 else None
    )

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=10000,
            sublinear_tf=True,
            strip_accents="unicode",
            analyzer="word",
            min_df=1,
        )),
        ("clf", LogisticRegression(
            C=1.0,
            max_iter=1000,
            multi_class="ovr",
            solver="lbfgs",
            random_state=42,
        )),
    ])

    logger.info(f"Training on {len(X_train)} examples, evaluating on {len(X_test)}")
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)
    report = classification_report(y_test, y_pred, zero_division=0)

    logger.info(f"New model F1 (weighted): {f1:.4f}")
    logger.info(f"Classification report:\n{report}")

    return pipeline, f1, report


def register_model(pipeline, f1: float, report: str, training_size: int):
    """Register model in MLflow and promote if it improves."""
    mlflow.set_tracking_uri(MLFLOW_URI)
    client = MlflowClient()

    current_f1 = get_current_production_f1()

    with mlflow.start_run(run_name=f"retraining-{datetime.now().strftime('%Y%m%d-%H%M')}") as run:
        # Log parameters
        mlflow.log_param("model_type",       "tfidf_logreg")
        mlflow.log_param("training_samples", training_size)
        mlflow.log_param("categories",       len(CATEGORIES))
        mlflow.log_param("timestamp",        datetime.now().isoformat())

        # Log metrics
        mlflow.log_metric("f1_weighted",     f1)
        mlflow.log_metric("previous_f1",     current_f1)
        mlflow.log_metric("f1_improvement",  f1 - current_f1)

        # Log the model
        mlflow.sklearn.log_model(
            pipeline,
            artifact_path="model",
            registered_model_name=MODEL_NAME,
        )

        run_id = run.info.run_id
        logger.info(f"Model logged with run_id: {run_id}")

    # Get the newly registered version
    versions = client.get_latest_versions(MODEL_NAME, stages=["None"])
    if not versions:
        logger.error("Model registration failed")
        return False

    new_version = versions[0].version
    logger.info(f"New model version: {new_version}")

    # Promote to production if F1 improves by more than MIN_F1_DELTA
    if f1 > current_f1 + MIN_F1_DELTA or current_f1 == 0.0:
        client.transition_model_version_stage(
            name=MODEL_NAME,
            version=new_version,
            stage="Production",
            archive_existing_versions=True,
        )
        logger.info(f"PROMOTED to Production: F1 {current_f1:.4f} → {f1:.4f} (+{f1-current_f1:.4f})")
        return True
    else:
        client.transition_model_version_stage(
            name=MODEL_NAME,
            version=new_version,
            stage="Staging",
        )
        logger.info(f"Kept in Staging: improvement {f1-current_f1:.4f} below threshold {MIN_F1_DELTA}")
        return False


def main():
    logger.info("=" * 60)
    logger.info("CIPHER Retraining Job started")
    logger.info("=" * 60)

    # Step 1: Load feedback from database
    feedback_df = load_feedback_from_db()

    # Step 2: Build training dataset
    df = build_training_data(feedback_df)

    if len(df) < MIN_SAMPLES:
        logger.warning(f"Only {len(df)} samples — minimum is {MIN_SAMPLES}. Using seed data to bootstrap.")

    # Step 3: Train model
    pipeline, f1, report = train_model(df)

    # Step 4: Register and conditionally promote
    promoted = register_model(pipeline, f1, report, len(df))

    logger.info("=" * 60)
    logger.info(f"Retraining complete — promoted={promoted} f1={f1:.4f}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
