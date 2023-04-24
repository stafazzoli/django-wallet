from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

from .models import BankAccount


def get_account(iban, user):
    if not (account := BankAccount.objects.filter(iban=iban, user=user, deleted_at=None).first()):
        raise ValidationError(_('Account does not belong to the user'))

    return account
