from decimal import Decimal

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator , MaxValueValidator


class Evento(models.Model):

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="eventos_creados"
    )
    event_name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    profit = models.IntegerField(default=80,validators=[MinValueValidator(75),MaxValueValidator(95)])
    min_bet_amount = models.DecimalField(max_digits=10 , decimal_places=2, default=Decimal("5.00"), validators=[MinValueValidator(Decimal("5.00"))])
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    event_date = models.DateTimeField(default=timezone.now,editable= False)

    class State (models.TextChoices):
        OPEN = "open", "Abierto"
        CLOSE = "close" , "Abierto"
        FINISHED = "finished","Finalizado"
    state = models.CharField(
        max_length=40,
        choices= State.choices,
        default=State.OPEN,
    )

    class Winner_Result (models.TextChoices):
        FIRST_OPTION = "first_option","primera_opcion"
        SECOND_OPTION = "second_option","segunda_opcion"
        DRAW = "draw","empate"

    winner_result = models.CharField(
        max_length=30,
        choices=Winner_Result.choices,
        blank=True,
    )


    close_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def is_open(self):
        return timezone.now() < self.close_date



class Category(models.Model):
    category = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["category"]
