from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from decimal import Decimal

from bets.models import Bet
from events.models import Evento
from wallet.models import Balance
from django.contrib.auth.models import User


@login_required
def making_bet(request):

    if request.method == "POST":
        user = request.user

        event_id = request.POST.get("event_id")
        choice = request.POST.get("choice")
        date_close = request.POST.get("date_close")
        bet_price = request.POST.get("bet_priece")

        evento = get_object_or_404(Evento, id=event_id)

        # Obtener o crear balance
        balance_obj, created = Balance.objects.get_or_create(user=user)

        bet_price = Decimal(bet_price)

        if bet_price <= balance_obj.balance:

            # Descontar saldo
            balance_obj.balance -= bet_price
            balance_obj.save()

            # Crear apuesta
            Bet.objects.create(
                user=user,
                event=evento,
                select_option=choice,
                date_close_bet=date_close
            )

            print("Apuesta creada con éxito")

        else:
            print("Saldo insuficiente")

        return redirect("bets:making_bet")

    # GET
    my_bets = Bet.objects.filter(user=request.user)
    print(request.user)

    return render(
        request,
        "bets.html",
        {"data": my_bets}
    )