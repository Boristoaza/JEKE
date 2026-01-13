from django.db import models
from django.conf import settings
from django.utils import timezone


class Evento(models.Model):

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="eventos_creados"
    )

    event_name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)

    event_date = models.DateTimeField(default=timezone.now,editable= False)
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
