from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from shinhan_api.demand_deposit import inquire_demand_deposit_account_list


User = get_user_model()

@api_view(['GET'])
@login_required
def index(request):
    user = request.user
    if request.method == 'GET':
        response = {'data': []}
        for i in inquire_demand_deposit_account_list(user.email)['REC']:
            response['data'].append({'bankName': i['bankName'], 'accountNo': i['accountNo'], 'accountBalance': i['accountBalance']})
        return Response(response, status=status.HTTP_200_OK)