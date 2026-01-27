import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json


stripe.api_key = settings.STRIPE_SECRET_KEY


def home(request):
    return render(request, 'master.html')


def pasarela(request):
    return render(request, 'pasarela.html')


def create_checkout_session(request):

    if request.method == "POST":
        amount = Decimal(request.POST.get("amount"))
        user_name = request.user.username
        amount = amount.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP
        )
        if amount < 10 or amount == 10:
             return redirect("/")
        else:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f"Hola {user_name} 👋 — Recarga de Jekes",
                        },
                        'unit_amount': int(amount * 100),
                    },
                    'quantity': 1,
                }],

                mode='payment',
                success_url=request.build_absolute_uri('/wallet/success/'),
                cancel_url=request.build_absolute_uri('/events/'),
            )
            return redirect(session.url)
@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except Exception as e:
        print("❌ Webhook error:", e)
        return HttpResponse(status=400)

    event_type = event["type"]
    print("📩 Evento:", event_type)

    if event_type == "checkout.session.completed":
        session = event["data"]["object"]

        payment_intent_id = session.get("payment_intent")
        if not payment_intent_id:
            print("⚠️ No payment_intent")
            return HttpResponse(status=200)

        # 👉 forma correcta
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        charge_id = payment_intent.latest_charge
        charge = stripe.Charge.retrieve(charge_id)

        balance_tx = stripe.BalanceTransaction.retrieve(
            charge.balance_transaction
        )

        print("✅ Pago exitoso")
        print("💰 Pagado:", balance_tx.amount / 100)
        print("🏦 Comisión Stripe:", balance_tx.fee / 100)
        print("📥 Neto recibido:", balance_tx.net / 100)

    return HttpResponse(status=200)


def success(request):
    return render(request, 'success.html')
