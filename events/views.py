from django.shortcuts import render
from django.http import HttpResponse
from users.selectors import get_events, get_search
from .models import Evento


def events_view(request):
    category_selected = request.GET.get("category_item")
    search_input = request.GET.get("search")

    if category_selected:
        events = get_events(category=category_selected)

    elif search_input:
        events = get_search(search=search_input)

    else:
        events = Evento.objects.all()[:10]

    return render(request, "events.html", {
        "events": events,
        "category_selected": category_selected,
        "search_input": search_input
    })

def detail_card_view(request):
    return render(request, "detail_card.html")