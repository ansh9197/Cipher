import logging
import re
from typing import Dict
from app.core.config import settings
from app.ml.model import get_model

logger = logging.getLogger(__name__)


# ── Rule-based fallback classifier ───────────────────────────────────────────
# This runs when no trained model is available in MLflow yet.
# As you collect labeled data and train, the ML model replaces these rules.

RULES = [
    {
        "category": "test_failure",
        "patterns": [
            r"AssertionError", r"FAILED tests/", r"pytest.*failed",
            r"\d+ failed", r"test.*FAILED", r"assertion.*failed",
            r"Expected.*but got", r"jest.*FAIL",
        ],
        "root_cause": "One or more automated tests failed. The code does not match the expected behavior.",
        "suggestion": "Check the test output for the specific assertion that failed. Review recent commits that touched the failing test file.",
    },
    {
        "category": "dependency_error",
        "patterns": [
            r"ModuleNotFoundError", r"ImportError", r"npm ERR!",
            r"yarn error", r"Cannot find module", r"No module named",
            r"pip.*error", r"requirements.*not found",
        ],
        "root_cause": "A required package or module could not be found or installed.",
        "suggestion": "Verify all dependencies are listed in requirements.txt or package.json. Check for typos in package names.",
    },
    {
        "category": "build_error",
        "patterns": [
            r"SyntaxError", r"compilation.*failed", r"build.*failed",
            r"error TS\d+", r"ERROR in ", r"make.*Error",
            r"gcc.*error", r"linker command failed",
        ],
        "root_cause": "The code could not be compiled or built due to a syntax or type error.",
        "suggestion": "Fix the syntax error reported above. Run the build locally to reproduce and debug.",
    },
    {
        "category": "auth_failure",
        "patterns": [
            r"Permission denied", r"Access denied", r"403 Forbidden",
            r"401 Unauthorized", r"authentication failed",
            r"credentials.*invalid", r"token.*expired",
            r"secret.*not found",
        ],
        "root_cause": "The pipeline could not authenticate with a required service.",
        "suggestion": "Check that all secrets (API keys, tokens, passwords) are correctly set in your repository's Settings → Secrets.",
    },
    {
        "category": "infra_error",
        "patterns": [
            r"Connection refused", r"ConnectionRefused",
            r"dial tcp.*refused", r"no such host",
            r"network.*unreachable", r"ECONNREFUSED",
            r"Could not connect to", r"failed to reach",
        ],
        "root_cause": "The pipeline could not connect to a required service (database, API, cache).",
        "suggestion": "Ensure service dependencies are started before tests run. Add health check steps or wait-for-it scripts.",
    },
    {
        "category": "timeout",
        "patterns": [
            r"timeout", r"timed out", r"Timeout",
            r"exceeded.*time", r"DeadlineExceeded",
            r"took too long",
        ],
        "root_cause": "A step or test exceeded its configured time limit.",
        "suggestion": "Increase the timeout setting or investigate what is causing the slowness. Profile the slow step locally.",
    },
]


def _rule_based_predict(log_text: str) -> Dict:
    """Apply ordered regex rules to classify the failure."""
    log_lower = log_text.lower()
    best_match = None
    best_count = 0

    for rule in RULES:
        count = sum(
            1 for p in rule["patterns"]
            if re.search(p, log_text, re.IGNORECASE)
        )
        if count > best_count:
            best_count = count
            best_match = rule

    if best_match and best_count > 0:
        confidence = min(0.5 + best_count * 0.1, 0.92)
        return {
            "category":   best_match["category"],
            "confidence": round(confidence, 2),
            "root_cause": best_match["root_cause"],
            "suggestion": best_match["suggestion"],
            "method":     "rule_based",
        }

    return {
        "category":   "unknown",
        "confidence": 0.40,
        "root_cause": "Could not determine the specific root cause from the available log output.",
        "suggestion": "Review the complete pipeline log. Check for error messages just before the failure step.",
        "method":     "rule_based",
    }


def predict(log_text: str, metadata: dict = None) -> Dict:
    """
    Main prediction function.
    Uses ML model if available, falls back to rule-based classifier.
    """
    model = get_model()

    if model is not None:
        try:
            import pandas as pd
            df = pd.DataFrame([{"log_text": log_text}])
            prediction = model.predict(df)
            logger.info(f"ML model prediction: {prediction}")
            return {
                "category":   str(prediction[0].get("category", "unknown")),
                "confidence": float(prediction[0].get("confidence", 0.80)),
                "root_cause": str(prediction[0].get("root_cause", "")),
                "suggestion": str(prediction[0].get("suggestion", "")),
                "method":     "ml_model",
            }
        except Exception as e:
            logger.error(f"ML model prediction failed: {e}, falling back to rules")

    return _rule_based_predict(log_text)
