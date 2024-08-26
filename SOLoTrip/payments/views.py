from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Payment
from trips.models import Member
from .serializers import PaymentCreateSerializer, PaymentDetailSerializer
from shinhan_api.demand_deposit import update_demand_deposit_account_withdrawal as withdrawal
from chatgpt_api.api import categorize

User = get_user_model()

@api_view(['POST'])
@login_required
def pay(request):
    # pay_date, pay_time에 bank_account 계좌에서 mutual에서 결제한 amount가 출금된다
    if request.method == 'POST':
        data = request.data
        bank_account = data.get('bank_account')
        amount = data.get('amount')
        
        member = Member.objects.filter(bank_account=bank_account)[0]
        email = member.user.email
        response = withdrawal(bank_account, amount, email)
        data['transaction_unique_number'] = response['REC']['transactionUniqueNo']
        data['transaction_type'] = '출금'

        # ChatGPT API를 이용하여 결제 내역의 카테고리를 저장한다
        data['category'] = categorize(data.get('brand_name'))

        serializer = PaymentCreateSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@login_required
def pay_list(request):
    if request.method == 'GET':
        # start_date~finish_date 까지의 trip_id와 연계된 bank_account 계좌'들'의 거래 내역을 조회한다
        # http://127.0.0.1:8000/payments/list?trip_id=11&start_date=2024-08-12&end_date=2024-12-12
        trip_id = request.GET.get('trip_id')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        members = Member.objects.filter(trip_id=trip_id)
        bank_accounts = members.values_list('bank_account', flat=True)
        
        payments = Payment.objects.filter(
            pay_date__gte=start_date, 
            pay_date__lte=end_date, 
            bank_account__in=bank_accounts
        )
        serializer = PaymentDetailSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
@api_view(["POST"])
@login_required
def settle(request):
    if request.method == 'POST':
        pass