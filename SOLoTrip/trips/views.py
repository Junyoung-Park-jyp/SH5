from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .serializers import TripSerializer, TripDetailSerializer, MemberCreateSerializer
from .models import Trip, Member
from django.utils import timezone


User = get_user_model()

@api_view(['POST', 'PUT'])
@login_required
def create_trip(request):
    if request.method == 'POST':
        serializer = TripSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            trip = serializer.save()
            data = {
                "trip": trip.pk, 
                "user": request.user.pk, 
                "bank_account": request.data.get('accountNo')
            }
            member_serializer =  MemberCreateSerializer(data=data)
            if member_serializer.is_valid(raise_exception=True):
                member_serializer.save()
            for username in request.data.get("members"):
                data = {
                    "trip": trip.pk, 
                    "user": User.objects.get(username=username).pk, 
                }
                member_serializer =  MemberCreateSerializer(data=data)
                if member_serializer.is_valid(raise_exception=True):
                    member_serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
    elif request.method == 'PUT':
        trip_id = request.data.get('tripId')
        try:
            trip = Trip.objects.get(pk=trip_id)
        except Trip.DoesNotExist:
            return Response({'error': 'Trip not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TripSerializer(trip, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            trip = serializer.save()
            # 기존 멤버와 새로운 멤버를 비교해서 추가해줘야하는데...
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
@login_required
def ongoing(request):
    if request.method == 'GET':
        current_date = timezone.now().date()
        trips = Trip.objects.filter(
            member__user=request.user,
            end_date__gte=current_date
        ).distinct()
        serializer = TripSerializer(trips, many=True)
        if serializer.data:
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'data': []}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@login_required
def finish(request):
    if request.method == 'GET':
        current_date = timezone.now().date()
        trips = Trip.objects.filter(
            member__user=request.user,
            end_date__lt=current_date
        ).distinct()
        serializer = TripSerializer(trips, many=True)
        if serializer.data:
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'data': serializer.data}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@login_required
def detail(request, trip_id):
    if request.method == 'GET':
        if not trip_id:
            return Response({'message': 'tripId가 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            trip = Trip.objects.get(pk=trip_id)
        except Trip.DoesNotExist:
            return Response({'message': 'Trip이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        members = Member.objects.filter(trip=trip_id, user=request.user)
        print(members)
        if not members:
            return Response({'message': "허가되지 않은 사용자입니다."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = TripDetailSerializer(trip)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@login_required
def invite(request):
    if request.method == 'POST':
        username = request.data.get('username')
        trip_id = request.data.get('tripId')

        # 사용자가 존재하는지 확인
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': '해당 사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        # 중복 체크: 이미 해당 trip과 user 조합이 존재하는지 확인
        if Member.objects.filter(trip_id=trip_id, user=user).exists():
            return Response({'error': '이 사용자는 이미 이 여행에 초대되었습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # Member 객체 생성
        data = {
            'trip': trip_id, 
            'user': user.pk, 
        }
        member_serializer = MemberCreateSerializer(data=data)
        if member_serializer.is_valid(raise_exception=True):
            member_serializer.save()
            return Response({'message': '멤버 초대가 완료되었습니다.'}, status=status.HTTP_201_CREATED)

        return Response(member_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        