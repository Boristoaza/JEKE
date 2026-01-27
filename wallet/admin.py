from django.contrib import admin
from wallet.models import Wallet_Transaction , Wallet
# Register your models here.
admin.site.register(Wallet)
admin.site.register(Wallet_Transaction)
