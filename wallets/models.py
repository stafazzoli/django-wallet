import uuid
from time import time

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, Case, When, F
from django.db.models.functions import Coalesce
from django.utils.crypto import get_random_string
from transitions import Machine, MachineError

from .errors import TransitionError
from .schemas import RequestKinds, RequestStates, transitions


class Wallet(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=True)

    class Meta:
        db_table = 'wallets'
        ordering = ['created_at']

    @property
    def balance(self):
        balance = Transaction.objects.filter(wallet=self).aggregate(
            balance=Coalesce(Sum('amount', output_field=models.BigIntegerField()), 0)
        )['balance']

        return balance

    @property
    def reserved_balance(self):
        reserved_balance = self.balance - \
                           TransactionRequest.objects.filter(account__in=self.user.user_accounts.all(),
                                                             kind=RequestKinds.Withdraw,
                                                             status=RequestStates.Init,
                                                             deleted_at=None).aggregate(
                               balance=Coalesce(Sum(
                                   Case(
                                       When(kind=RequestKinds.Deposit, then=F('amount')),
                                       When(kind=RequestKinds.Withdraw, then=-F('amount'))
                                   ),
                                   output_field=models.IntegerField()), 0)
                           )['balance']

        return reserved_balance

    def __str__(self):
        return str(self.user)


class Transaction(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    wallet = models.ForeignKey(Wallet, on_delete=models.DO_NOTHING)
    account = models.ForeignKey('banks.BankAccount', on_delete=models.DO_NOTHING)
    amount = models.BigIntegerField()
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transactions'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.wallet} - {self.amount}'


def create_request_number():
    return int(str(int(time() * 10)) + get_random_string(length=3, allowed_chars="0123456789"))


class TransactionRequest(models.Model):
    kinds = [(k, k.value) for k in RequestKinds]
    statuses = [(r, r.value) for r in RequestStates]

    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    number = models.BigIntegerField(unique=True, null=False, default=create_request_number)
    kind = models.CharField(max_length=10, choices=kinds, default=RequestKinds.Withdraw)
    status = models.CharField(max_length=10, null=False, choices=statuses, default=RequestStates.Init)
    amount = models.BigIntegerField()
    account = models.ForeignKey('banks.BankAccount', on_delete=models.DO_NOTHING)

    scheduled_at = models.DateTimeField()
    transaction = models.OneToOneField(Transaction, null=True, blank=True, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'transaction_requests'
        ordering = ['created_at']

    def __str__(self):
        return str(self.number)

    def change_state(self, trigger):
        state_machine = Machine(model='self',
                                states=RequestStates,
                                initial=str(self.status),
                                transitions=transitions,
                                queued=True)
        try:
            state_machine.dispatch(trigger)
            self.status = state_machine.state.value
        except MachineError as e:
            raise TransitionError()
