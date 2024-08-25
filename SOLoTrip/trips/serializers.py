from rest_framework import serializers
from .models import Trip, Location, Member
from django.contrib.auth import get_user_model

User = get_user_model()

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['country', 'city']

class MemberNameSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    class Meta:
        model = Member
        fields = ['username', 'bank_account']

class TripCreateSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, write_only=True)
    members = MemberNameSerializer(many=True, write_only=True)

    class Meta:
        model = Trip
        fields = ['trip_name', 'start_date', 'end_date', 'locations', 'members']

    def create(self, validated_data):
        locations_data = validated_data.pop('locations')
        members_data = validated_data.pop('members')

        # Trip 객체 생성
        trip = Trip.objects.create(**validated_data)

        # Location 데이터 생성
        for location_data in locations_data:
            Location.objects.create(trip=trip, **location_data)

        # Member 데이터 생성
        for member_data in members_data:
            username = member_data['username']
            bank_account = member_data['bank_account']
            try:
                user = User.objects.get(username=username)
                Member.objects.create(trip=trip, user=user, bank_account=bank_account)
            except User.DoesNotExist:
                continue

        return trip

    def update(self, instance, validated_data):
        print(validated_data)
        # 기존 Location과 Member 삭제
        Location.objects.filter(trip=instance).delete()
        Member.objects.filter(trip=instance).delete()

        locations_data = validated_data.pop('locations')
        members_data = validated_data.pop('members')

        # Trip의 기본 필드를 업데이트
        instance.trip_name = validated_data.get('trip_name', instance.trip_name)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.save()

        # 새로운 Location 데이터 추가
        for location_data in locations_data:
            Location.objects.create(trip=instance, **location_data)

        # 새로운 Member 데이터 추가
        for member_data in members_data:
            username = member_data['user']['username']
            bank_account = member_data['bank_account']
            try:
                user = User.objects.get(username=username)
                Member.objects.create(trip=instance, user=user, bank_account=bank_account)
            except User.DoesNotExist:
                continue

        return instance


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = "__all__"
        
        
class MemberDetailSerializer(serializers.ModelSerializer):
    member = serializers.CharField(source='user.username')
    class Meta:
        model = Member
        fields = ['member', 'bank_account', 'is_participate', 'budget']
        
        
class TripMainSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, read_only=True)
    members = MemberDetailSerializer(many=True, read_only=True)
    class Meta:
        model = Trip
        fields = ['start_date', 'end_date', 'locations', 'members']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['locations'] = LocationSerializer(instance.location_set.all().order_by('country', 'city'), many=True).data
        representation['members'] = MemberDetailSerializer(instance.member_set.all().order_by('user__username'), many=True).data
        return representation
