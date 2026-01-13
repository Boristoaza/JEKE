from datetime import timezone
from urllib import request
from events.models import Evento,Category
from users.models import Image
from django.http import HttpResponse
from django.db.models import Q

# llama a todas los eventos de apuestas
def get_events(*, category):
   if category:
    return Evento.objects.filter(category=category).values()
   else:
    return Evento.objects.all().values()

# llama solo a las categorias
def get_categorys():
  return Category.objects.all().values()

def get_search(*, search):
    if not search:
        return Evento.objects.none()

    return Evento.objects.filter(
        Q(category__icontains=search) |
        Q(event_name__icontains=search) |
        Q(first_name__icontains=search) |
        Q(second_name__icontains=search) |
        Q(description__icontains=search)
    ).values()

def get_image_profile(request):
    if not request.user.is_authenticated:
        return None
    return Image.objects.filter(user_id=request.user.id).order_by("-id").first()
