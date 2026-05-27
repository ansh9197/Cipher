import logging, uuid
from datetime import datetime
logger = logging.getLogger(__name__)

async def save_analysis_to_db(result: dict):
    try:
        import asyncpg
        from app.core.config import settings
        db_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
        conn = await asyncpg.connect(db_url)
        try:
            row = await conn.fetchrow("SELECT id FROM users ORDER BY created_at LIMIT 1")
            if not row:
                logger.warning("No users found, skipping DB save")
                return
            await conn.execute("""
                INSERT INTO analyses (id,tenant_id,run_id,repo,branch,workflow_name,
                conclusion,category,confidence,root_cause,suggestion,method,created_at)
                VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13)
                ON CONFLICT (id) DO NOTHING
            """, str(uuid.uuid4()), str(row["id"]),
                str(result.get("run_id","")), result.get("repo",""),
                result.get("branch","main"), result.get("workflow_name","CI"),
                result.get("conclusion","failure"), result.get("category","unknown"),
                float(result.get("confidence",0)), result.get("root_cause",""),
                result.get("suggestion",""), result.get("method","rule_based"),
                datetime.utcnow())
            logger.info(f"Saved to DB: {result.get('repo')} {result.get('category')}")
        finally:
            await conn.close()
    except Exception as e:
        logger.error(f"DB save failed: {e}")
