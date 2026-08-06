import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_product(name):
    """Создание продукта в Stripe."""
    try:
        product = stripe.Product.create(
            name=name,
        )
        return product
    except stripe.error.StripeError as e:
        print(f"Ошибка создания продукта: {e}")
        return None


def create_price(product_id, amount):
    """Создание цены для продукта в Stripe."""
    try:
        price = stripe.Price.create(
            product=product_id,
            unit_amount=amount,  # в копейках
            currency='rub',
        )
        return price
    except stripe.error.StripeError as e:
        print(f"Ошибка создания цены: {e}")
        return None


def create_checkout_session(price_id):
    """Создание сессии для оплаты."""
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url='http://127.0.0.1:8000/success/',
            cancel_url='http://127.0.0.1:8000/cancel/',
        )
        return checkout_session
    except stripe.error.StripeError as e:
        print(f"Ошибка создания сессии: {e}")
        return None
