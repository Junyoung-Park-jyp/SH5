from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import BankAccounts


User = get_user_model()

class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccounts
        fields = ['account_number', 'balance', 'fixed_balance', 'bank']
        
        
class BankAccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccounts
        fields = ['account_number', 'balance', 'fixed_balance', 'bank']