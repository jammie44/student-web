from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db
from app.core.security import get_current_user
from app.core.config import settings

router = APIRouter(prefix="/api/billing", tags=["billing"])


class CheckoutRequest(BaseModel):
    price_id: str
    success_url: str
    cancel_url: str


@router.post("/create-checkout")
def create_checkout(req: CheckoutRequest, current_user=Depends(get_current_user)):
    if not settings.stripe_secret_key:
        raise HTTPException(status_code=503, detail="Billing is not configured.")
    try:
        import stripe
        stripe.api_key = settings.stripe_secret_key
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            line_items=[{"price": req.price_id, "quantity": 1}],
            success_url=req.success_url,
            cancel_url=req.cancel_url,
            customer_email=current_user.email,
        )
        return {"checkout_url": session.url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    if not settings.stripe_webhook_secret:
        raise HTTPException(status_code=503, detail="Webhook not configured.")
    try:
        import stripe
        stripe.api_key = settings.stripe_secret_key
        payload = await request.body()
        sig = request.headers.get("stripe-signature")
        event = stripe.Webhook.construct_event(payload, sig, settings.stripe_webhook_secret)
        if event["type"] == "customer.subscription.created":
            from app.models.user import User
            from app.models.subscription import Subscription
            data = event["data"]["object"]
            user = db.query(User).filter(User.email == data.get("customer_email")).first()
            if user:
                sub = Subscription(user_id=user.id, stripe_sub_id=data["id"],
                                   stripe_customer_id=data.get("customer"), status=data["status"], plan="pro")
                db.add(sub)
                db.commit()
        return {"received": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
