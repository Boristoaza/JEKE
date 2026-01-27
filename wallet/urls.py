from django.urls import path
from . import views

app_name = "wallet"

urlpatterns = [
    path('', views.create_checkout_session, name='wallet_pay'),
    path('success/',views.success , name="success"),
    path('stripe/webhook/', views.stripe_webhook),
]
