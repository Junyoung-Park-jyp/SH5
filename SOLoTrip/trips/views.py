from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .serializers import TripCreateSerializer, TripSerializer, TripMainSerializer, MemberDetailSerializer
from .models import Trip, Member, Location
from django.utils import timezone
from accounts.serializers import UserSerializer


User = get_user_model()

@api_view(['POST', 'PUT'])
@login_required
def create_trip(request):
    if request.method == 'POST':
        serializer = TripCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            trip = serializer.save()
            Member.objects.create(trip=trip, user=request.user, bank_account=request.data.get('bank_account'))
            return Response({'data': {"id": trip.pk}}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        trip_id = request.data.get('trip_id')
        try:
            trip = Trip.objects.get(pk=trip_id)
        except Trip.DoesNotExist:
            return Response({'error': 'Trip not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TripCreateSerializer(trip, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            trip = serializer.save()
            return Response({'data': {"id": trip.pk}}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # elif request.method == 'DELETE':
    #     trip_id = request.data.get('trip_id')
    #     try:
    #         trip = Trip.objects.get(pk=trip_id)
    #     except Trip.DoesNotExist:
    #         return Response({'error': 'Trip not found'}, status=status.HTTP_404_NOT_FOUND)
    #     trip_name = trip.username
    #     trip.delete()
    #     return Response({"message": f"{trip_name} 여행이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        

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
        return Response({'error': "예정되거나 진행중인 여행이 없습니다."}, status=status.HTTP_204_NO_CONTENT)


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
        return Response({'error': "완료된 여행이 없습니다."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@login_required
def trip_main(request):
    if request.method == 'GET':
        trip_id = request.GET.get('trip_id')
        try:
            trip = Trip.objects.get(pk=trip_id)
        except Trip.DoesNotExist:
            return Response({'error': '해당 아이디에 해당하는 Trip이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TripMainSerializer(trip)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@login_required
def member(request):
    if request.method == 'GET':
        email = request.GET.get('email')
        try:
            user = User.objects.get(email=email)
        except:
            return Response({"error": "해당 이메일을 사용하는 사용자가 없습니다."}, status=status.HTTP_204_NO_CONTENT)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        email = request.data.get('email')
        trip_id = request.data.get('trip_id')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': '해당 사용자를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        trip = Trip.objects.get(pk=trip_id)
        if Member.objects.filter(trip=trip, user=user).exists():
            return Response({'error': '이 사용자는 이미 이 여행에 초대되었습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        Member.objects.create(trip=trip, user=user)
        members = Member.objects.filter(trip=trip)
        serializer = MemberDetailSerializer(members, many=True)
        data = serializer.data
        return Response({'data': data}, status=status.HTTP_201_CREATED)
    
    
@api_view(['PUT'])
@login_required
def budget(request):
    if request.method == 'PUT':
        trip_id = request.data.get('trip_id')
        budget = request.data.get('budget')
        member = Member.objects.get(trip_id=trip_id, user=request.user)
        member.budget = budget
        member.save()
        return Response({'data': {'budget': budget}}, status=status.HTTP_202_ACCEPTED)
        