from rest_framework import status
from rest_framework.exceptions import APIException


class DepositAmountNotValidError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Deposit amount must be greater than zero'


class WithdrawAmountGreaterThanBalanceError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'User wallet reserved balance is lower than requested amount'


class TransitionError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Cannot change request state'


class DepositScheduleRequiredError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'It is required to set the schedule for deposit requests'
