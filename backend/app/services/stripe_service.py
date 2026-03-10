import stripe
from backend.app.core.config import settings

stripe.api_key = settings.stripe_secret_key


def create_checkout_session(price_id: str, user_email: str) -> str:
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='subscription',
        success_url='http://localhost:3000/success',
        cancel_url='http://localhost:3000/cancel',
        customer_email=user_email,
    )
    return session.url


def handle_webhook(payload: str, sig: str) -> dict:
    endpoint_secret = settings.stripe_webhook_secret
    event = stripe.Webhook.construct_event(payload, sig, endpoint_secret)
    return event


def cancel_subscription(subscription_id: str):
    stripe.Subscription.delete(subscription_id)


def get_subscription_status(subscription_id: str) -> str:
    subscription = stripe.Subscription.retrieve(subscription_id)
    return subscription.status