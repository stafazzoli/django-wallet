import logging

import requests
from celery import shared_task
from decouple import config
from rest_framework import status
from tenacity import TryAgain, retry, stop_after_attempt, retry_if_exception_type

from wallet.configs import ConfigKeys
from .models import TransactionRequest, Wallet, Transaction
from .schemas import RequestKinds, RequestTransitions


@retry(stop=stop_after_attempt(3), retry=retry_if_exception_type(TryAgain))
def call_bank():
    res = requests.post(url=config(ConfigKeys.BankURL))
    if res.json().get('status') != status.HTTP_200_OK:
        raise TryAgain
    else:
        return res.json().get('data')


@shared_task()
def process_request(request_number: int):
    if not (request := TransactionRequest.objects.filter(number=request_number, deleted_at=None) \
            .select_related('account').first()):
        logging.error('Failed to find transaction request %d to apply', request_number)
        return

    if request.kind == RequestKinds.Withdraw.value:
        wallet = Wallet.objects.get(user=request.account.user)
        transaction = Transaction.objects.create(
            wallet=wallet,
            account=request.account,
            amount=-request.amount,
            description=f'withdrew {request.amount}'
        )
        request.change_state(RequestTransitions.Success)
        request.transaction = transaction

    elif request.kind == RequestKinds.Deposit.value:
        try:
            call_bank()
        except:
            logging.error('Failed to call bank')
            request.change_state(RequestTransitions.Fail)
        else:
            wallet = Wallet.objects.get(user=request.account.user)
            transaction = Transaction.objects.create(
                wallet=wallet,
                account=request.account,
                amount=request.amount,
                description=f'deposited {request.amount}'
            )

            request.change_state(RequestTransitions.Success)
            request.transaction = transaction

    request.save()
