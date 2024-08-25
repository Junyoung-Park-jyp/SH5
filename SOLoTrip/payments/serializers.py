from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Payment
from trips.models import Member
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
    account_owner = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = ['amount', 'pay_date', 'pay_time', 'mutual', 'category', 'bank_account', 'transaction_type', 'account_owner', 'transaction_unique_number']

    def get_account_owner(self, obj):
        # 해당 Payment의 bank_account와 연결된 Member를 통해 사용자를 찾습니다.
        try:
            member = Member.objects.filter(bank_account=obj.bank_account)[0]
            return member.user.email  # 여기서 사용자의 이름이나 원하는 정보를 반환합니다.
        except Member.DoesNotExist:
            return None  # 해당 bank_account를 가진 Member가 없을 경우 None 반환

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        bank_account = representation['bank_account']
        transaction_unique_number = representation['transaction_unique_number']

        # transaction_unique_number를 응답에서 제거
        representation.pop('transaction_unique_number')

        # balance 추가
        email = Member.objects.filter(bank_account=bank_account)[0].user.email
        print(email)
        response = transaction(bank_account, transaction_unique_number, email)['REC']['transactionAfterBalance']
        print(response)
        representation['balance'] = transaction(bank_account, transaction_unique_number, email)['REC']['transactionAfterBalance']
        return representation

        