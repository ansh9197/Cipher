import httpx
import logging
import time
import jwt as pyjwt
from app.core.config import settings
from typing import Optional

logger = logging.getLogger(__name__)


def _load_private_key() -> Optional[str]:
    try:
        with open(settings.github_app_private_key_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        logger.warning("GitHub App private key not found — using placeholder mode")
        return None


def _make_jwt() -> Optional[str]:
    key = _load_private_key()
    if not key or not settings.github_app_id:
        return None
    now = int(time.time())
    payload = {"iat": now - 60, "exp": now + 600, "iss": settings.github_app_id}
    return pyjwt.encode(payload, key, algorithm="RS256")


async def get_installation_token(installation_id: str) -> Optional[str]:
    """Exchange GitHub App JWT for an installation access token."""
    app_jwt = _make_jwt()
    if not app_jwt:
        return None

    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url,
            headers={
                "Authorization": f"Bearer {app_jwt}",
                "Accept":        "application/vnd.github+json",
            },
            timeout=15,
        )
        if resp.status_code == 201:
            return resp.json().get("token")
        logger.error(f"Failed to get installation token: {resp.status_code} {resp.text}")
        return None


async def download_run_logs(
    repo: str,
    run_id: str,
    installation_id: Optional[str] = None,
) -> Optional[str]:
    """
    Download the raw log text for a GitHub Actions workflow run.
    Returns plain text or None on failure.
    """
    token = await get_installation_token(installation_id) if installation_id else None

    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"token {token}"

    url = f"https://api.github.com/repos/{repo}/actions/runs/{run_id}/logs"

    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            resp = await client.get(url, headers=headers, timeout=30)
            if resp.status_code == 200:
                return resp.text
            logger.error(f"Log download failed: {resp.status_code} for {repo}/{run_id}")
            return None
        except Exception as e:
            logger.error(f"Exception downloading logs: {e}")
            return None


async def post_pr_comment(
    repo: str,
    pr_number: int,
    body: str,
    installation_id: Optional[str] = None,
) -> bool:
    """Post a comment on a GitHub PR."""
    token = await get_installation_token(installation_id) if installation_id else None
    if not token:
        logger.warning("No installation token — skipping PR comment")
        return False

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(
                url,
                headers={
                    "Authorization": f"token {token}",
                    "Accept":        "application/vnd.github+json",
                },
                json={"body": body},
                timeout=15,
            )
            return resp.status_code == 201
        except Exception as e:
            logger.error(f"Failed to post PR comment: {e}")
            return False
