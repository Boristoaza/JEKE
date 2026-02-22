from django.contrib import admin
from wallet.models import Wallet_Transaction , Payment,Balance
# Register your models here.
admin.site.register(Payment)
admin.site.register(Wallet_Transaction)
admin.site.register(Balance)
