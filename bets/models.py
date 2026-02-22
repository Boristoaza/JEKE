from django.db import models
from events.models import Evento
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator , MaxValueValidator
from decimal import Decimal


class Bet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bets")
    event = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="bets")
    select_option = models.CharField(max_length=255)
    profit = models.IntegerField(default=80,validators=[MinValueValidator(75),MinValueValidator(95)])
    min_bet_amount = models.DecimalField(max_digits=10 , decimal_places=2, default=Decimal("5.00"), validators=[MinValueValidator(Decimal("5.00"))])
    date_made_bet = models.DateTimeField(auto_now_add=True)
    date_close_bet = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'event'],
                name='unique_bet_per_user_event'
            )
        ]
