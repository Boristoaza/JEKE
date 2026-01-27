from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name_image = models.CharField(
        max_length=255,
        default="default_image"
    )
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"{self.name_image} {self.user}"
