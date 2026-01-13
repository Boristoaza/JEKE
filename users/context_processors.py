from events.models import Category
from users.selectors import get_events

def site_info(request):
  categorys = Category.objects.all().values()
  all_info = {"category":categorys }

  return all_info
