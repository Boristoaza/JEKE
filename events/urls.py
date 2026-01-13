from django.urls import path
from . import views


app_name = "events"

urlpatterns = [
    path('', views.events_view, name='event_list'),
    path('detail/', views.detail_card_view, name='detail_card'),
]
