from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Payment
from shinhan_api.demand_deposit import inquire_transaction_history as transaction

User = get_user_model()


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['amount', 'pay_date', 'pay_time', 'mutual', 'category', 'bank_account', 'transaction_unique_number', 'transaction_type']
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('transaction_unique_number')
        return representation
        
        
class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['amount', 'pay_date', 'pay_time', 'mutual', 'category', 'bank_account', 'transaction_unique_number', 'transaction_type']
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        bank_account = representation['bank_account']
        transaction_unique_number = representation['transaction_unique_number']
        representation.pop('transaction_unique_number')
        representation['balance'] = transaction(bank_account, transaction_unique_number)['REC']['transactionAfterBalance']
        return representation
        