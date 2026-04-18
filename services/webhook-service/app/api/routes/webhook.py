from fastapi import APIRouter, Request, HTTPException, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from app.core.config import settings
from app.core.kafka import publish_event
import hmac
import hashlib
import json
import logging
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()


def verify_github_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verify GitHub HMAC webhook signature."""
    if not signature or not signature.startswith("sha256="):
        return False
    expected = "sha256=" + hmac.new(
        secret.encode("utf-8"),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected, signature)


@router.post("/github")
async def github_webhook(
    request: Request,
    x_github_event: Optional[str] = Header(None),
    x_hub_signature_256: Optional[str] = Header(None),
    x_github_delivery: Optional[str] = Header(None),
):
    raw_body = await request.body()

    # 1. Verify signature
    if settings.app_env != "development":
        if not verify_github_signature(raw_body, x_hub_signature_256 or "", settings.github_webhook_secret):
            logger.warning(f"Invalid webhook signature from GitHub delivery {x_github_delivery}")
            raise HTTPException(status_code=401, detail="Invalid signature")

    # 2. Only handle workflow_run events
    if x_github_event != "workflow_run":
        return {"status": "ignored", "reason": f"event type '{x_github_event}' not handled"}

    try:
        payload = json.loads(raw_body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    action      = payload.get("action")
    workflow    = payload.get("workflow_run", {})
    conclusion  = workflow.get("conclusion")
    status      = workflow.get("status")
    run_id      = workflow.get("id")
    repo        = payload.get("repository", {})
    repo_name   = repo.get("full_name", "unknown/unknown")
    installation= payload.get("installation", {})
    install_id  = installation.get("id")

    logger.info(f"workflow_run event: repo={repo_name} action={action} conclusion={conclusion} run_id={run_id}")

    # 3. Only process completed + failed runs
    if action != "completed" or conclusion not in ("failure", "timed_out", "startup_failure"):
        return {"status": "ignored", "reason": f"conclusion={conclusion} not a failure"}

    # 4. Build the event payload for the analysis service
    event = {
        "event_type":       "pipeline_failed",
        "run_id":           str(run_id),
        "repo":             repo_name,
        "repo_id":          str(repo.get("id", "")),
        "branch":           workflow.get("head_branch", ""),
        "commit_sha":       workflow.get("head_sha", ""),
        "workflow_name":    workflow.get("name", ""),
        "conclusion":       conclusion,
        "html_url":         workflow.get("html_url", ""),
        "logs_url":         workflow.get("logs_url", ""),
        "installation_id":  str(install_id) if install_id else None,
        "triggered_at":     datetime.utcnow().isoformat(),
        "pull_requests":    [
            {
                "number": pr.get("number"),
                "url":    pr.get("url"),
                "head":   pr.get("head", {}).get("ref"),
            }
            for pr in workflow.get("pull_requests", [])
        ],
    }

    # 5. Publish to Kafka
    published = publish_event(
        topic="pipeline-failures",
        key=f"{repo_name}:{run_id}",
        payload=event,
    )

    if not published:
        logger.error(f"Failed to queue analysis for run {run_id}")
        raise HTTPException(status_code=503, detail="Failed to queue analysis")

    logger.info(f"Queued analysis for {repo_name} run {run_id}")
    return {
        "status":   "queued",
        "run_id":   str(run_id),
        "repo":     repo_name,
        "topic":    "pipeline-failures",
    }
