from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, UserCreationSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from shinhan_api.member import signup as shinhan_signup, search
from django.contrib.auth import get_user_model


User = get_user_model()

@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        email = request.data.get('email')
        username = email.split("@")[0]
        password = 'rkskekfk'  # 이 프로젝트에서 사용자는 비밀번호가 필요없으므로 기본값 설정
        data = {
            "username": username, "password": password, "email": email
        }
        serializer = UserCreationSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            response = shinhan_signup(email)
            if "responseCode" in response:
                return Response(response, status=status.HTTP_409_CONFLICT)
            serializer.save(user_key=response['userKey'])
        return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        username = email.split("@")[0]
        try:
            user = User.objects.get(username=username)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        auth_login(request, user)
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def logout(request):
    if request.method == "POST":
        auth_logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','PUT'])
def profile(request):
    user = get_user_model().objects.get(pk=request.user.pk)
    if request.method == 'GET':
        seriazlier = UserSerializer(user)
        return Response(seriazlier.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        if user != request.user:
            return Response({'message': 'disallowed'})
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        