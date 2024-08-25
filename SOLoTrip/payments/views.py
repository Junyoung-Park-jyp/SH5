from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Payment
from .serializers import PaymentCreateSerializer, PaymentDetailSerializer
from shinhan_api.demand_deposit import update_demand_deposit_account_withdrawal as withdrawal
from shinhan_api.demand_deposit import inquire_transaction_history_list as transaction_list


User = get_user_model()

@api_view(['POST'])
@login_required
def pay(request):
    # pay_date, pay_time에 bank_account 계좌에서 mutual에서 결제한 amount가 출금된다
    if request.method == 'POST':
        data = request.data
        bank_account = data.get('bank_account')
        amount = data.get('amount')
        response = withdrawal(bank_account, amount)
        data['transaction_unique_number'] = response['REC']['transactionUniqueNo']
        data['transaction_type'] = '출금'
        serializer = PaymentCreateSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@login_required
def pay_list(request):
    if request.method == 'GET':
        # start_date~finish_date 까지의 bank_account 계좌의 거래 내역을 조회한다
        # http://127.0.0.1:8000/payments/list?bank_account=0817158183605808&start_date=2024-08-12&end_date=2024-12-12
        bank_account = request.GET.get('bank_account')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        payments = Payment.objects.filter(
            pay_date__gte=start_date, 
            pay_date__lte=end_date, 
            bank_account=bank_account
        )
        serializer = PaymentDetailSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)