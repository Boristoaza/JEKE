from django.urls import path
from . import views

app_name = "bets"

urlpatterns = [
    path("", views.making_bet, name="making_bet"),
]
