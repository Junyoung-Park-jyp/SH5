from rest_framework import serializers
from .models import Trip, Member, Location
from django.contrib.auth import get_user_model

User = get_user_model()

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['country', 'city']


class MemberSerializer(serializers.ModelSerializer):
    member = serializers.CharField(source='user.username')

    class Meta:
        model = Member
        fields = ['member']


class TripCreateSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True)
    members = MemberSerializer(many=True)
    accountNo = serializers.CharField(write_only=True)

    class Meta:
        model = Trip
        fields = ['start_date', 'end_date', 'budget', 'accountNo', 'locations', 'members']

    def create(self, validated_data):
        # Trip 데이터를 먼저 생성
        locations_data = validated_data.pop('locations')
        members_data = validated_data.pop('members')
        account_no = validated_data.pop('accountNo')

        trip = Trip.objects.create(**validated_data)

        # Location 데이터 생성
        for location_data in locations_data:
            Location.objects.create(trip=trip, **location_data)

        # Member 데이터 생성: members에 포함된 user들을 참조하여 Member 객체 생성
        for member_data in members_data:
            username = member_data['user']['username']
            try:
                user = User.objects.get(username=username)
                Member.objects.create(trip=trip, user=user, bank_account=account_no)
            except User.DoesNotExist:
                continue  # 존재하지 않는 사용자에 대한 처리 어떻게 하지 흠

        request_user = self.context['request'].user
        Member.objects.create(trip=trip, user=request_user, bank_account=account_no)

        return trip
