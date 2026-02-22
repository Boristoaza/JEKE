
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


def registrar_view(request): #listo funcion traducida
    if request.method == "POST":
        nombre_usuario = request.POST.get("username", "").strip()
        correo = request.POST.get("email", "").strip()
        contrasena = request.POST.get("password")
        confirmar_contrasena = request.POST.get("confirm_password")

        # validar contraseñas
        if contrasena != confirmar_contrasena:
            messages.error(request, "Las contraseñas no coinciden")
            return render(request, "register.html")

        # validar usuario existente
        if User.objects.filter(username=nombre_usuario).exists():
            messages.error(request, "El usuario ya existe")
            return render(request, "register.html")

        # crear usuario
        usuario = User.objects.create_user(
            username=nombre_usuario,
            email=correo,
            password=contrasena
        )

        # login automático
        login(request, usuario)

        messages.success(request, "Usuario registrado correctamente")
        return redirect("profile")

    return render(request, "register.html")

def login_view(request):
    if request.method == "POST":
        identificador = request.POST.get("username", "").strip()
        contrasena = request.POST.get("password")

        user = authenticate(
            request,
            username=identificador,
            password=contrasena
        )

        # intentar por email
        if user is None:
            try:
                usuario_obj = User.objects.get(email__iexact=identificador)
                user = authenticate(
                    request,
                    username=usuario_obj.username,
                    password=contrasena
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
