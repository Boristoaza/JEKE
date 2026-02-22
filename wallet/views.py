import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from django.contrib.auth.decorators import login_required

from wallet.models import Payment , Balance
from django.db.models import F


stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRET



def home(request):
    return render(request, 'master.html')


def pasarela(request):
    return render(request, 'pasarela.html')


@login_required
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

                payment_intent_data={
                    "metadata": {
                        "id_customer": str(request.user.pk),
                        "username": request.user.username,
                    }
                },
                success_url=request.build_absolute_uri('/wallet/success/'),
                cancel_url=request.build_absolute_uri('/events/'),
            )
            return redirect(session.url)


@csrf_exempt
def stripe_webhook(request):
  payload = request.body
  event = None

  try:
    event = stripe.Event.construct_from(
      json.loads(payload), stripe.api_key
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)

  if endpoint_secret:
        sig_header = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except stripe.error.SignatureVerificationError as e:
            print('⚠️  Webhook signature verification failed.' + str(e))
            return HttpResponse(success=False)

  # Handle the event
  if event.type == 'payment_intent.succeeded':

    payment_intent = event.data.object
    id_costumer = int(payment_intent.metadata.id_customer)
    username= payment_intent.metadata.username
    amount=payment_intent.amount / 100
    try:
        Payment.objects.create(
            user_id=int(id_costumer),
            username=username,
            amount=amount
        )
        print("Guardado exitoso")
        Balance.objects.get_or_create(user_id=int(id_costumer))

        Balance.objects.filter(user_id=int(id_costumer)).update(
            balance=F("balance") + amount
        )
        print("gracias por su compra suerte")
    except ValueError:
        print("ID inválido")
        return HttpResponse(status=400)

    except Exception as e:
        print(f"Error real: {e}")
        return HttpResponse(status=500)

  elif event.type == 'payment_method.attached':
    payment_method = event.data.object
  else:
    print('Unhandled event type {}'.format(event.type))
  return HttpResponse(status=200)





def success(request):
    return render(request, 'success.html')
