from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserCreationSerializer, UserSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from shinhan_api.member import signup as shinhan_signup, search
from shinhan_api.demand_deposit import create_demand_deposit_account


User = get_user_model()

@api_view(['POST'])
def signup(request):
    email = request.data.get('email')
    username = request.data.get('username')
    password = 'rkskekfk'
    data = {
        "username": username, "password": password, "email": email
    }
    serializer = UserCreationSerializer(data=data)
    response = shinhan_signup(email)
    if 'userKey' in response:
        data['user_key'] = response['userKey']
    else:
        data['user_key'] = search(email)['userKey']

    if serializer.is_valid():
        user = serializer.save()
        create_demand_deposit_account(email)
        serializer = UserSerializer(user)
        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response({"error": "이미 존재하는 사용자 이메일 혹은 닉네임입니다."}, status=status.HTTP_409_CONFLICT)

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "확인되지 않는 사용자 이메일입니다."}, status=status.HTTP_404_NOT_FOUND)
    
    auth_login(request, user)
    serializer = UserSerializer(user)
    return Response({"data": serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    auth_logout(request)
    return Response({"message": "로그아웃 완료"}, status=status.HTTP_204_NO_CONTENT)
