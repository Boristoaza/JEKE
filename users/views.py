
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from datetime import datetime

from users.selectors import get_image_profile


from events.models import Evento , Category
# from users.models import Image
from .selectors import get_events , get_categorys , get_search


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # validar contraseñas
        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden")
            return render(request, "register.html")

        # validar usuario existente
        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe")
            return render(request, "register.html")

        # crear usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # login automático
        login(request, user)

        messages.success(request, "Usuario registrado correctamente")
        return redirect("profile")

    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        identifier = request.POST.get("username", "").strip()
        password = request.POST.get("password")
        user = authenticate(
            request,
            username=identifier,
            password=password
        )

        if user is None:
            try:
                user_obj = User.objects.get(email__iexact=identifier)
                user = authenticate(
                    request,
                    username=user_obj.username,
                    password=password
                )
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            return redirect("profile")

        return render(request, "login.html", {
            "error": "Usuario o contraseña incorrectos"
        })

    return render(request, "login.html")

@login_required
def profile_view(request):

    image_profile = get_image_profile(request)

    context = {
        "image": image_profile
    }

    return render(request, "profile.html", context)

@require_POST
def logout_view(request):
   logout(request)
   return redirect("/")


def market_view(request):
  template = loader.get_template('market.html')
  return HttpResponse(template.render())


def master_view(request):
    events = Evento.objects.order_by("?")[:6]
    context = {
        "events": events,
    }
    return render(request, "master.html", context)

def test_view(request, id):
    event = Evento.objects.filter(id=id).values().first()
    return render(request, 'test.html', {'event': event})
