import asyncio
import json
import logging
import httpx
from confluent_kafka import KafkaError
from app.core.kafka import get_consumer, publish_event
from app.core.log_parser import parse_log
from app.core.github_client import download_run_logs
from app.core.config import settings

logger = logging.getLogger(__name__)

FAILURE_TOPIC    = "pipeline-failures"
RESULT_TOPIC     = "analysis-results"
CONSUMER_GROUP   = "analysis-workers"


def format_pr_comment(result: dict, event: dict) -> str:
    """Build the markdown comment posted to the PR."""
    category   = result.get("category",   "unknown")
    confidence = result.get("confidence", 0.0)
    root_cause = result.get("root_cause", "Could not determine root cause.")
    suggestion = result.get("suggestion", "Please review the logs manually.")
    run_url    = event.get("html_url",    "#")

    stars = int(confidence * 5)
    conf_bar = "★" * stars + "☆" * (5 - stars)

    return f"""## CIPHER — Pipeline Failure Analysis

**Failure category:** `{category}`
**Confidence:** {conf_bar} ({confidence:.0%})

### Root cause
{root_cause}

### Suggested fix
{suggestion}

---
<sub>Analyzed by [CIPHER](https://cipher.dev) · [View run]({run_url}) · Was this helpful? React 👍 or 👎</sub>
"""


async def call_inference(log_text: str, metadata: dict) -> dict:
    """Call the inference service to get the analysis."""
    url = f"{settings.inference_service_url}/api/v1/predict"
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                url,
                json={
                    "log_text": log_text,
                    "metadata": metadata,
                },
                timeout=60,
            )
            if resp.status_code == 200:
                return resp.json()
            logger.error(f"Inference service error: {resp.status_code}")
            return _fallback_analysis(log_text)
    except Exception as e:
        logger.error(f"Could not reach inference service: {e}")
        return _fallback_analysis(log_text)


def _fallback_analysis(log_text: str) -> dict:
    """
    Rule-based fallback when inference service is unavailable.
    Ensures users always get SOME analysis.
    """
    log_lower = log_text.lower()

    if "modulenotfounderror" in log_lower or "importerror" in log_lower:
        return {
            "category":   "dependency_error",
            "confidence": 0.75,
            "root_cause": "A Python module could not be imported. This is usually a missing dependency in requirements.txt or a virtual environment issue.",
            "suggestion": "Run `pip install -r requirements.txt` and verify the package name is spelled correctly.",
        }
    if "npm err!" in log_lower or "yarn error" in log_lower:
        return {
            "category":   "dependency_error",
            "confidence": 0.75,
            "root_cause": "Node package installation failed.",
            "suggestion": "Delete node_modules and package-lock.json, then run `npm install` again.",
        }
    if "connectionrefused" in log_lower or "connection refused" in log_lower:
        return {
            "category":   "infra_error",
            "confidence": 0.70,
            "root_cause": "A service connection was refused. A database or external service may not have started before the test ran.",
            "suggestion": "Add a health check wait step before running tests. Use `wait-for-it.sh` or a retry loop.",
        }
    if "timeout" in log_lower or "timed out" in log_lower:
        return {
            "category":   "timeout",
            "confidence": 0.70,
            "root_cause": "A step exceeded its time limit.",
            "suggestion": "Increase the timeout value or investigate what is causing the slowness.",
        }
    if "assertionerror" in log_lower or "assertion failed" in log_lower or "fail" in log_lower:
        return {
            "category":   "test_failure",
            "confidence": 0.65,
            "root_cause": "One or more tests failed. The assertion did not match the expected value.",
            "suggestion": "Review the failing test output above, check recent code changes that may have affected this test.",
        }
    if "permission denied" in log_lower or "access denied" in log_lower:
        return {
            "category":   "auth_failure",
            "confidence": 0.72,
            "root_cause": "A permission or authentication error occurred.",
            "suggestion": "Verify that all required secrets and environment variables are set in your GitHub repository settings.",
        }

    return {
        "category":   "build_error",
        "confidence": 0.50,
        "root_cause": "The pipeline failed. Could not determine a specific root cause automatically.",
        "suggestion": "Review the full log output for error messages. Check recent commits for syntax errors or breaking changes.",
    }


async def process_event(event: dict):
    """Full analysis pipeline for one failure event."""
    run_id    = event.get("run_id")
    repo      = event.get("repo")
    install_id= event.get("installation_id")

    logger.info(f"Processing failure: repo={repo} run={run_id}")

    # 1. Download logs from GitHub
    raw_log = await download_run_logs(repo, run_id, install_id)

    if not raw_log:
        # Use metadata as fallback context
        raw_log = f"Pipeline failed for {repo}\nWorkflow: {event.get('workflow_name')}\nConclusion: {event.get('conclusion')}\nBranch: {event.get('branch')}"
        logger.warning(f"Could not download logs for {repo}/{run_id}, using metadata")

    # 2. Parse and clean the log
    parsed = parse_log(raw_log)
    focused_log = parsed["focused_log"]

    logger.info(f"Log parsed: {parsed['total_lines']} lines → {parsed['error_count']} errors found")

    # 3. Call inference service
    result = await call_inference(
        log_text=focused_log,
        metadata={
            "repo":          repo,
            "workflow_name": event.get("workflow_name", ""),
            "branch":        event.get("branch", ""),
            "conclusion":    event.get("conclusion", ""),
        },
    )

    logger.info(f"Analysis complete: category={result.get('category')} confidence={result.get('confidence')}")

    # 4. Publish result to analysis-results topic
    output_event = {
        **event,
        "analysis":   result,
        "pr_comment": format_pr_comment(result, event),
        "log_stats":  parsed,
    }
    publish_event(
        topic=RESULT_TOPIC,
        key=f"{repo}:{run_id}",
        payload=output_event,
    )

    return result


def start_consumer():
    """
    Blocking Kafka consumer loop.
    Runs as a background thread alongside the FastAPI server.
    """
    consumer = get_consumer(CONSUMER_GROUP)
    consumer.subscribe([FAILURE_TOPIC])
    logger.info(f"Analysis worker listening on topic: {FAILURE_TOPIC}")

    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() != KafkaError._PARTITION_EOF:
                logger.error(f"Kafka consumer error: {msg.error()}")
            continue

        try:
            event = json.loads(msg.value().decode("utf-8"))
            asyncio.run(process_event(event))
            consumer.commit(msg)
        except Exception as e:
            logger.error(f"Failed to process event: {e}")
