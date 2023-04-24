from django.utils.translation import gettext as _
from rest_framework import serializers

from .models import Wallet, TransactionRequest
from .utils import get_current_date


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('uuid', 'user', 'balance', 'created_at')
        read_only_fields = ('uuid', 'balance', 'created_at')


class CreateRequestSerializer(serializers.ModelSerializer):
    account = serializers.CharField(source='BankAccount.iban')
    scheduled_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = TransactionRequest
        fields = ('uuid', 'number', 'account', 'amount', 'scheduled_at', 'created_at')
        read_only_fields = ('uuid', 'number', 'scheduled_at')

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError(_('amount should be greater than zero.'))

        return value

    def validate_scheduled_at(self, value):
        if value and value < get_current_date():
            raise serializers.ValidationError(_('date should be greater than now.'))

        return value
