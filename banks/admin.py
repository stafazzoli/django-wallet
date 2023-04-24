from django.contrib import admin

from banks.models import Bank, BankAccount

admin.site.register(Bank)
admin.site.register(BankAccount)
