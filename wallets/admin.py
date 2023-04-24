from django.contrib import admin

from .models import Wallet, TransactionRequest, Transaction

admin.site.register(Wallet)
admin.site.register(TransactionRequest)
admin.site.register(Transaction)
