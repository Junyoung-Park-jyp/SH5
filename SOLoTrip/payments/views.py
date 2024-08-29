from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Payment, Calculate
from trips.models import Member
from .serializers import PaymentCreateSerializer, PaymentDetailSerializer, CalculateCreateSerializer
from shinhan_api.demand_deposit import update_demand_deposit_account_withdrawal as withdrawal
from shinhan_api.demand_deposit import update_demand_deposit_account_Transfer as transfer
from shinhan_api.demand_deposit import inquire_demand_deposit_account_balance as balance
from chatgpt_api.api import categorize


User = get_user_model()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pay(request):
    # pay_date, pay_time에 bank_account 계좌에서 brand_name에서 결제한 amount가 출금된다
    if request.method == 'POST':
        data = request.data
        bank_account = data.get('bank_account')
        amount = data.get('amount')
        
        member = Member.objects.filter(bank_account=bank_account)[0]
        
        if request.user != member.user:
            return Response({'error': "현재 사용자는 해당 계좌의 주인이 아닙니다."}, status=status.HTTP_401_UNAUTHORIZED)

        email = member.user.email
        response = withdrawal(bank_account, amount, email)
        data['transaction_unique_number'] = response['REC']['transactionUniqueNo']
        data['transaction_type'] = '출금'
        
        # ChatGPT API를 이용하여 결제 내역의 카테고리를 저장한다
        try:
            data['category'] = categorize(data.get('brand_name'))
        except:
            data['category'] = "미정"

        serializer = PaymentCreateSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pay_list(request):
    if request.method == 'GET':
        # start_date~finish_date 까지의 trip_id와 연계된 bank_account 계좌'들'의 거래 내역을 조회한다
        trip_id = request.GET.get('trip_id')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        if not Member.objects.filter(trip=trip_id, user=request.user).exists():
            return Response({'error': "현재 사용자는 해당 여행에 참여하지 않았습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        
        members = Member.objects.filter(trip_id=trip_id)
        bank_accounts = members.values_list('bank_account', flat=True)
        
        payments = Payment.objects.filter(
            pay_date__gte=start_date, 
            pay_date__lte=end_date, 
            bank_account__in=bank_accounts
        ).order_by('pay_date', 'pay_time')
        serializer = PaymentDetailSerializer(payments, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def adjustment(request):
    if request.method == 'POST':
        # trip_id에 떠있는 결제 내역을 클릭하면 정산할 수 있고, 멤버별 값을 결정할 수 있다.
        # 필요 데이터: trip_id, {member별 정산 금액과 bank_account}, payment_id
        payments = request.data.get('payments')
        for payment in payments:    
            payment_id = payment.get('payment_id')
            if Calculate.objects.filter(payment_id=payment_id).exists():
                return Response({'error': "이미 정산이 완료된 정산이 포함되었습니다."}, status=status.HTTP_403_FORBIDDEN)
            bank_account = Payment.objects.get(id=payment_id).bank_account
            if not Member.objects.filter(bank_account=bank_account, user=request.user).exists():
                return Response({'error': "현재 사용자는 해당 계좌를 사용하고 있지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = CalculateCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            result = serializer.save()
            return Response({'data': result}, status=status.HTTP_201_CREATED)
        
        
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def objection(request):
    if request.method == 'POST':
        # trip_id에 떠있는 결제 내역을 클릭하면 취소할 수 있다.
        # 필요 데이터: payment_id
        trip_id = request.data.get('trip_id')
        payment_id = request.data.get('payment_id')
        calculates = Calculate.objects.filter(payment=payment_id)
        
        if not Member.objects.filter(trip=trip_id, user=request.user).exists():
            return Response({'error': "현재 사용자는 해당 여행에 참여하지 않았습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        
        members = Member.objects.filter(trip=trip_id)
        result = {}
        for member in members:
            if member.bank_account:
                result[member.user.username] = {"before_balance": int(balance(member.user.email, member.bank_account)['REC']['accountBalance'])}  # 정산 전 잔액

        payment = Payment.objects.get(id=payment_id)
        withdrawal_bank_account = payment.bank_account
        withdrawal_user = Member.objects.filter(bank_account=withdrawal_bank_account)[0].user
        withdrawal_email = withdrawal_user.email
        username = withdrawal_user.username
        # result[username] = {"before_balance": int(balance(withdrawal_email, withdrawal_bank_account)['REC']['accountBalance'])}
        for calculate in calculates:
            deposit_user = calculate.member
            deposit_bank_account = deposit_user.bank_account
            transfer(withdrawal_email, deposit_bank_account, withdrawal_bank_account, calculate.cost)
        
        for member in members:
            if member.bank_account:
                username = member.user.username
                temp_balance = int(balance(member.user.email, member.bank_account)['REC']['accountBalance'])
                initial_balance = result[username]["before_balance"]
                result[username]["difference"] = temp_balance - initial_balance  # 정산 전후 차액
                result[username]["after_balance"] = temp_balance  # 정산 후 잔액
        
        calculates.delete()
        return Response({'data': result}, status=status.HTTP_204_NO_CONTENT)