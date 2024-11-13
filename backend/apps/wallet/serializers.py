
from rest_framework import serializers

from .models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    """ Кошелек. """

    class Meta:
        model = Wallet
        fields = ['balance']

class TransactionSerializer(serializers.Serializer):
    """ Транзакция. """

    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
