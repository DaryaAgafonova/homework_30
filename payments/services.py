import stripe
from django.conf import settings
from .models import StripePayment

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_product(name: str) -> dict:
    return stripe.Product.create(name=name)

def create_price(product_id: str, amount: int) -> dict:
    return stripe.Price.create(
        product=product_id,
        unit_amount=amount,
        currency='usd',
    )

def create_session(price_id: str, success_url: str, cancel_url: str) -> dict:
    return stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )

def retrieve_session(session_id: str) -> dict:
    return stripe.checkout.Session.retrieve(session_id)

def create_payment_record(
    user,
    course,
    stripe_product_id: str,
    stripe_price_id: str,
    session_id: str,
    checkout_url: str,
    amount: float
) -> StripePayment:
    return StripePayment.objects.create(
        user=user,
        course=course,
        stripe_product_id=stripe_product_id,
        stripe_price_id=stripe_price_id,
        session_id=session_id,
        checkout_url=checkout_url,
        amount=amount
    )

def update_payment_status(payment: StripePayment, status: str) -> StripePayment:
    payment.status = status
    payment.save()
    return payment 