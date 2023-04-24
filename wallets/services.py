from datetime import timedelta, datetime
from zoneinfo import ZoneInfo

from banks.services import get_account
from .errors import WithdrawAmountGreaterThanBalanceError, DepositScheduleRequiredError
from .models import TransactionRequest, Wallet
from .schemas import RequestKinds
from .tasks import process_request
from .utils import get_current_date


def get_wallet_reserved_balance(user):
    wallet = Wallet.objects.get(user=user)
    return wallet.reserved_balance


def create_request(user, kind, data):
    data['account'] = get_account(data['account'], user)

    if kind == RequestKinds.Deposit and not data.get('scheduled_at'):
        raise DepositScheduleRequiredError()

    if kind == RequestKinds.Withdraw and data['amount'] > Wallet.objects.get(user=user).reserved_balance:
        raise WithdrawAmountGreaterThanBalanceError()

    if data.get('scheduled_at'):
        data['scheduled_at'] = datetime.strptime(data.get('scheduled_at'), '%Y-%m-%d %H:%M:%S') \
            .astimezone(ZoneInfo('UTC'))
    else:
        data['scheduled_at'] = get_current_date()

    request: TransactionRequest = TransactionRequest.objects.create(kind=kind, **data)

    process_request.apply_async(kwargs={'request_number': request.number},
                                eta=request.scheduled_at + timedelta(seconds=5))
