from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Wallet(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  balance = models.PositiveIntegerField(default=0)

  def __str__(self):
      return f"{self.user.username} - {self.balance} JEKE"

class Wallet_Transaction(models.Model):
    TRANSACTION_TYPE = (
        ('deposit', 'Depósito'),
        ('bet', 'Apuesta'),
        ('win', 'Ganancia'),
        ('withdraw', 'Retiro'),
    )

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount = models.IntegerField()
    type = models.CharField(max_length=20,choices=TRANSACTION_TYPE)
    reference = models.CharField(max_length=225,blank=True , null=True)

    def __str__(self):
       return f"{self.user} {self.amount} {self.type} {self.reference}"
