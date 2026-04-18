from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.config import settings
from app.models.user import User, PlanType
from app.api.routes.users import get_current_user
import stripe, logging

logger = logging.getLogger(__name__)
router = APIRouter()
stripe.api_key = settings.stripe_secret_key

PLAN_PRICES = {
    "starter": settings.stripe_price_starter,
    "pro":     settings.stripe_price_pro,
}

@router.get("/plans")
async def get_plans():
    return {"plans": [
        {"id": "free",    "name": "Free",    "price_usd": 0,  "analyses": 50,   "repos": 1},
        {"id": "starter", "name": "Starter", "price_usd": 29, "analyses": 500,  "repos": 5},
        {"id": "pro",     "name": "Pro",     "price_usd": 99, "analyses": -1,   "repos": -1},
    ]}

@router.post("/create-checkout")
async def create_checkout(plan: str, current_user: User = Depends(get_current_user)):
    if plan not in PLAN_PRICES or not PLAN_PRICES[plan]:
        raise HTTPException(status_code=400, detail="Invalid plan or Stripe not configured")
    try:
        session = stripe.checkout.Session.create(
            customer_email=current_user.email,
            mode="subscription",
            line_items=[{"price": PLAN_PRICES[plan], "quantity": 1}],
            success_url=f"{settings.frontend_url}/dashboard?upgraded=true",
            cancel_url=f"{settings.frontend_url}/pricing",
            metadata={"user_id": str(current_user.id), "plan": plan}
        )
        return {"checkout_url": session.url}
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/webhook")
async def stripe_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    payload    = await request.body()
    sig_header = request.headers.get("stripe-signature", "")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.stripe_webhook_secret)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if event["type"] == "checkout.session.completed":
        meta    = event["data"]["object"]["metadata"]
        result  = await db.execute(select(User).where(User.id == meta["user_id"]))
        user    = result.scalar_one_or_none()
        if user:
            user.plan = PlanType(meta["plan"])
            user.stripe_customer_id     = event["data"]["object"].get("customer")
            user.stripe_subscription_id = event["data"]["object"].get("subscription")
            await db.flush()
            logger.info(f"{user.email} upgraded to {meta['plan']}")

    elif event["type"] == "invoice.payment_failed":
        cust_id = event["data"]["object"]["customer"]
        result  = await db.execute(select(User).where(User.stripe_customer_id == cust_id))
        user    = result.scalar_one_or_none()
        if user:
            user.plan = PlanType.free
            await db.flush()
            logger.warning(f"{user.email} downgraded — payment failed")

    return {"received": True}
