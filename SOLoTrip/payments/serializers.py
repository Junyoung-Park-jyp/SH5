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

    class Meta:
        model = Payment
        fields = "__all__"

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
        response = transaction(bank_account, transaction_unique_number, email)['REC']['transactionAfterBalance']
        representation['balance'] = transaction(bank_account, transaction_unique_number, email)['REC']['transactionAfterBalance']
        return representation


class CalculateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calculate
        fields = "__all__"


class BillSerializer(serializers.Serializer):
    cost = serializers.IntegerField()
    bank_account = serializers.CharField(max_length=30)


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
        trip_id = validated_data['trip_id']
        bills_data = validated_data['bills']
        payment_id = validated_data['payment_id']
        
        payment = Payment.objects.get(id=payment_id)
        deposit_bank_account = payment.bank_account
        calculate_instances = []
        
        for bill_data in bills_data:
            cost = bill_data['cost']
            withdrawal_bank_account = bill_data['bank_account']

            try:
                member = Member.objects.get(trip=trip_id, bank_account=withdrawal_bank_account)
            except Member.DoesNotExist:
                continue  # 해당 멤버가 없을 경우 이 bill을 건너뜁니다.
            except Payment.DoesNotExist:
                continue  # 해당 결제 내역이 없을 경우 이 bill을 건너뜁니다.

            # Calculate 객체 생성
            calculate_instance = Calculate.objects.create(
                payment=payment,
                member=member,
                cost=cost
            )
            calculate_instances.append(calculate_instance)
            response = transfer(member.user.email, deposit_bank_account, withdrawal_bank_account, cost)
            print(response)
        return calculate_instances