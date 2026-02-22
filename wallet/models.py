from django.db import models
from django.contrib.auth.models import User


# registro de pagos
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.amount} monedas"

# esta es la del saldo
class Balance (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="balance")
    balance = models.DecimalField(max_digits=12,decimal_places=2,default=0)
    def __str__(self):
        return f"{self.balance}"


class Wallet_Transaction(models.Model): #esto no tomes en cuenta
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
