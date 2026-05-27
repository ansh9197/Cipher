from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api.routes import health, feedback
from app.core.kafka import get_consumer
from app.core.github_commenter import post_pr_comment
import threading
from app.core.db_save import save_analysis_to_db
import asyncio
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RESULT_TOPIC   = "analysis-results"
CONSUMER_GROUP = "notification-workers"


async def handle_result(event: dict):
    """Process one analysis result and send the PR comment."""
    repo         = event.get("repo", "")
    pr_comment   = event.get("pr_comment", "")
    install_id   = event.get("installation_id")
    pull_requests= event.get("pull_requests", [])

    if not pull_requests:
        logger.info(f"No PRs found for {repo} run {event.get('run_id')} — skipping comment")
        return

    for pr in pull_requests:
        pr_number = pr.get("number")
        if pr_number:
            await post_pr_comment(
                repo=repo,
                pr_number=pr_number,
                body=pr_comment,
                installation_id=install_id,
            )


def start_consumer():
    consumer = get_consumer(CONSUMER_GROUP)
    consumer.subscribe([RESULT_TOPIC])
    logger.info(f"Notification worker listening on: {RESULT_TOPIC}")

    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            continue
        try:
            event = json.loads(msg.value().decode("utf-8"))
            asyncio.run(handle_result(event))
            consumer.commit(msg)
        except Exception as e:
            logger.error(f"Notification error: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Notification service starting...")
    thread = threading.Thread(target=start_consumer, daemon=True)
    thread.start()
    yield
    logger.info("Notification service shutting down...")


app = FastAPI(
    title="CIPHER Notification Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router,   tags=["health"])
app.include_router(feedback.router, prefix="/api/v1", tags=["feedback"])


@app.get("/")
async def root():
    return {"service": "cipher-notification", "status": "running"}
