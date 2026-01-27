from django.urls import path
from . import views


app_name = "events"

urlpatterns = [
    path('', views.events_view, name='event_list'), #ESTE LISTA TODAS LA CARDS
    path('detail/', views.detail_card_view, name='detail_card'), #ESTO NO TOMES EN CUENTA
]
