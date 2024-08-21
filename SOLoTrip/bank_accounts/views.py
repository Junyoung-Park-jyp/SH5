from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .serializers import BankAccountSerializer, BankAccountCreateSerializer
from .models import BankAccounts


User = get_user_model()

@api_view(['GET', "POST"])
@login_required
def index(request):
    user = request.user
    if request.method == 'GET':
        bank_accounts = BankAccounts.objects.filter(user=user)
        serializer = BankAccountSerializer(bank_accounts)
        return Response(serializer.data, status=status.HTTP_200_OK, many=True)
    elif request.method == 'POST':
        serializer = BankAccountCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)