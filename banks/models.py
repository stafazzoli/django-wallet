import uuid as uuid

from django.contrib.auth.models import User
from django.db import models


class Bank(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'banks'
        ordering = ['created_at']

    def __str__(self):
        return self.slug


class BankAccount(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    bank = models.ForeignKey(Bank, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='user_accounts')
    iban = models.CharField(max_length=34, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'bank_accounts'
        ordering = ['created_at']

    def __str__(self):
        return self.iban
