from fastapi import APIRouter, Depends, HTTPException, Request
from backend.app.core.security import get_current_user
from backend.app.models.user import User
from backend.app.services.stripe_service import create_checkout_session, handle_webhook
from backend.app.models.subscription import Subscription
from sqlalchemy.orm import Session
from backend.app.core.database import get_db

router = APIRouter()

@router.post("/create-checkout")
def create_checkout(price_id: str, current_user: User = Depends(get_current_user)):
    url = create_checkout_session(price_id, current_user.email)
    return {"checkout_url": url}

@router.post("/webhook")
async def stripe_webhook(request: Request, db: Session = Depends(get_db)):
    payload = await request.body()
    sig = request.headers.get('stripe-signature')
    try:
        event = handle_webhook(payload, sig)
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            customer_email = session.get('customer_email')
            subscription_id = session.get('subscription')
            # find user
            user = db.query(User).filter(User.email == customer_email).first()
            if user:
                sub = Subscription(user_id=user.id, stripe_subscription_id=subscription_id, status='active')
                db.add(sub)
                db.commit()
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))