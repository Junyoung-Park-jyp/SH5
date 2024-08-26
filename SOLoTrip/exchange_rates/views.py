from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from shinhan_api.exchange_rate import exchange_rate


User = get_user_model()

@api_view(['GET'])
@login_required
def index(request):
    user = request.user
    if request.method == 'GET':
        response = exchange_rate(user.email)['REC']
        return Response({"data": response}, status=status.HTTP_200_OK)