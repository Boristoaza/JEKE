from events.models import Category
from users.selectors import get_events
from wallet.models import Payment , Balance
from django.contrib.auth.models import User
from django.db.models import Sum


def site_info(request):
  categorys = Category.objects.all().values()
  user_id = request.user.id


  balance = Balance.objects.get(user=request.user).balance

  all_info = {"category":categorys , "balance":balance}

  return all_info
