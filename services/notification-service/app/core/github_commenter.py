import httpx
import time
import logging
import jwt as pyjwt
from app.core.config import settings
from typing import Optional

logger = logging.getLogger(__name__)


def _load_private_key() -> Optional[str]:
    try:
        with open(settings.github_app_private_key_path) as f:
            return f.read()
    except FileNotFoundError:
        logger.warning("GitHub App private key not found")
        return None


async def _get_installation_token(installation_id: str) -> Optional[str]:
    key = _load_private_key()
    if not key or not settings.github_app_id:
        return None

    now = int(time.time())
    token = pyjwt.encode(
        {"iat": now - 60, "exp": now + 600, "iss": settings.github_app_id},
        key,
        algorithm="RS256",
    )

    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
            },
            timeout=15,
        )
        if resp.status_code == 201:
            return resp.json().get("token")
    return None


async def post_pr_comment(
    repo: str,
    pr_number: int,
    body: str,
    installation_id: Optional[str] = None,
) -> bool:
    token = await _get_installation_token(installation_id) if installation_id else None
    if not token:
        logger.info(f"[DEV MODE] Would post to PR #{pr_number} on {repo}:\n{body[:200]}...")
        return True  # In dev mode, just log it

    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            url,
            headers={
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github+json",
            },
            json={"body": body},
            timeout=15,
        )
        success = resp.status_code == 201
        if success:
            logger.info(f"Posted PR comment on {repo}#{pr_number}")
        else:
            logger.error(f"Failed to post PR comment: {resp.status_code}")
        return success
