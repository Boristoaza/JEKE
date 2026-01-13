from django.shortcuts import render, redirect, get_object_or_404
from bets.models import Bet
from events.models import Evento
from django.contrib.auth.decorators import login_required


@login_required
def making_bet(request):

    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        user = request.user
        event_id = request.POST.get("event_id")
        choice = request.POST.get("choice")
        date_close = request.POST.get("date_close")  # 👈 YA viene bien

        evento = get_object_or_404(Evento, id=event_id)

        Bet.objects.create(
            user=user,
            event=evento,
            select_option=choice,
            date_close_bet=date_close  # 👈 directo
        )

        return redirect("bets:making_bet")

    user_id = request.user.id
    my_bets = Bet.objects.filter(user=user_id)

    data = {
        "data":my_bets
    }

    return render(request, "bets.html",data)
