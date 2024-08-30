from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Payment, Calculate
from trips.models import Member
from shinhan_api.demand_deposit import update_demand_deposit_account_Transfer as transfer
from shinhan_api.demand_deposit import inquire_demand_deposit_account_balance as balance

User = get_user_model()


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['amount', 'pay_date', 'pay_time', 'brand_name', 'category', 'bank_account']
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation
    
    
class CalculateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='member.user.username', read_only=True)
    
    class Meta:
        model = Calculate
        fields = ['username', 'cost']
        
        
class PaymentDetailSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()
    
    class Meta:
        model = Payment
        fields = "__all__"

    def get_is_completed(self, obj):
        return 1 if Calculate.objects.filter(payment=obj).exists() else 0

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        bank_account = representation['bank_account']

        user = Member.objects.filter(bank_account=bank_account).first().user
        representation['username'] = user.username
        
        calculates = Calculate.objects.filter(payment=instance)
        if calculates.exists():
            representation['is_completed'] = 1
            representation['calculates'] = CalculateSerializer(calculates, many=True).data
        else:
            representation['is_completed'] = 0
        return representation


class BillSerializer(serializers.Serializer):
    cost = serializers.IntegerField()
    bank_account = serializers.CharField(max_length=30)


class PaymentSerializer(serializers.Serializer):
    payment_id = serializers.IntegerField()
    bills = serializers.ListField(child=BillSerializer())


class CalculateCreateSerializer(serializers.Serializer):
    trip_id = serializers.IntegerField()
    payments = serializers.ListField(child=PaymentSerializer())

    def create(self, validated_data):
        trip_id = validated_data['trip_id']
        
        # 정산 전 금액을 계산하기 위해 결과 딕셔너리 초기화
        members = Member.objects.filter(trip=trip_id)
        result = {}
        for member in members:
            if member.bank_account:
                result[member.user.username] = {"before_balance": int(balance(member.user.email, member.bank_account)['REC']['accountBalance'])}  # 정산 전 잔액

        # 각 payment에 대해 처리
        for payment_data in validated_data['payments']:
            payment_id = payment_data['payment_id']
            bills_data = payment_data['bills']
            
            payment = Payment.objects.get(id=payment_id)
            deposit_bank_account = payment.bank_account
            
            for bill_data in bills_data:
                cost = bill_data['cost']
                withdrawal_bank_account = bill_data['bank_account']
                
                try:
                    member = Member.objects.get(trip=trip_id, bank_account=withdrawal_bank_account)
                except Member.DoesNotExist:
                    continue

                # Calculate 객체 생성
                Calculate.objects.create(
                    payment=payment,
                    member=member,
                    cost=cost
                )
                
                if deposit_bank_account == withdrawal_bank_account:  # 정산 가격만 기록하고 금액 전송은 안함
                    continue
                if cost == 0 or cost == '0':
                    continue
                # 금액 이체 로직 호출
                transfer(member.user.email, deposit_bank_account, withdrawal_bank_account, cost)
        
        # 정산 후 금액을 계산하기 위해 다시 members를 순회
        for member in members:
            if member.bank_account:
                username = member.user.username
                temp_balance = int(balance(member.user.email, member.bank_account)['REC']['accountBalance'])
                initial_balance = result[username]["before_balance"]
                result[username]["difference"] = temp_balance - initial_balance  # 정산 전후 차액
                result[username]["after_balance"] = temp_balance  # 정산 후 잔액

        return result