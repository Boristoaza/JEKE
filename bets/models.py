from django.db import models
from events.models import Evento
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator , MaxValueValidator
from decimal import Decimal


class Bet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bets")
    event = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="bets")
    select_option = models.CharField(max_length=255)
    date_made_bet = models.DateTimeField(auto_now_add=True)
    date_close_bet = models.DateTimeField(null=True , blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'event'],
                name='unique_bet_per_user_event'
            )
        ]
