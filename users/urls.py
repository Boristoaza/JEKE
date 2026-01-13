from django.urls import path
from . import views

urlpatterns = [
    path("", views.master_view , name="master"),
    path('market', views.market_view, name="market"),
    path('ex/',views.ex_view,name="ex"),
    path('profile/', views.profile_view, name="profile"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register_view, name='register'),

]