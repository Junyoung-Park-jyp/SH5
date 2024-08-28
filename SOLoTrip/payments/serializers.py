from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Payment, Calculate
from trips.models import Member
from shinhan_api.demand_deposit import inquire_transaction_history as transaction
from shinhan_api.demand_deposit import update_demand_deposit_account_Transfer as transfer

User = get_user_model()


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['amount', 'pay_date', 'pay_time', 'brand_name', 'category', 'bank_account', 'transaction_unique_number', 'transaction_type']
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('transaction_unique_number')
        return representation
        
        
class PaymentDetailSerializer(serializers.ModelSerializer):
    account_owner = serializers.SerializerMethodField()
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = "__all__"

    def get_account_owner(self, obj):
        try:
            member = Member.objects.filter(bank_account=obj.bank_account).first()
            return member.user.email if member else None
        except Member.DoesNotExist:
            return None

    def get_is_completed(self, obj):
        return 1 if Calculate.objects.filter(payment=obj).exists() else 0

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        bank_account = representation['bank_account']
        transaction_unique_number = representation['transaction_unique_number']

        representation.pop('transaction_unique_number')

        email = Member.objects.filter(bank_account=bank_account).first().user.email
        representation['balance'] = transaction(bank_account, transaction_unique_number, email)['REC']['transactionAfterBalance']

        return representation


class CalculateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calculate
        fields = "__all__"


class BillSerializer(serializers.Serializer):
    cost = serializers.IntegerField()
    bank_account = serializers.CharField(max_length=30)


class CalculateCreateSerializer(serializers.Serializer):
    trip_id = serializers.IntegerField()
    bills = serializers.ListField(
        child=BillSerializer()
    )
    payment_id = serializers.IntegerField()

    def create(self, validated_data):
        calculate_instances = []
        
        for data in validated_data:
            trip_id = data['trip_id']
            bills_data = data['bills']
            payment_id = data['payment_id']
            
            payment = Payment.objects.get(id=payment_id)
            deposit_bank_account = payment.bank_account
            
            for bill_data in bills_data:
                cost = bill_data['cost']
                withdrawal_bank_account = bill_data['bank_account']

                try:
                    member = Member.objects.get(trip=trip_id, bank_account=withdrawal_bank_account)
                except Member.DoesNotExist:
                    continue  # 해당 멤버가 없을 경우 이 bill을 건너뜁니다.

                # Calculate 객체 생성
                calculate_instance = Calculate.objects.create(
                    payment=payment,
                    member=member,
                    cost=cost
                )
                calculate_instances.append(calculate_instance)
                response = transfer(member.user.email, deposit_bank_account, withdrawal_bank_account, cost)
        return calculate_instances
