from rest_framework import serializers
from .models import Trip, Member, Location
from django.contrib.auth import get_user_model

User = get_user_model()

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['country', 'city']


class MemberNameSerializer(serializers.ModelSerializer):
    member = serializers.CharField(source='user.username')

    class Meta:
        model = Member
        fields = ['member']


class TripCreateSerializer(serializers.ModelSerializer):
    locations = LocationSerializer(many=True, write_only=True)
    members = MemberNameSerializer(many=True, write_only=True)
    bank_account = serializers.CharField(write_only=True)

    class Meta:
        model = Trip
        fields = ['trip_name', 'start_date', 'end_date', 'bank_account', 'locations', 'members']

    def create(self, validated_data):
        # Trip 데이터를 먼저 생성
        locations_data = validated_data.pop('locations')
        members_data = validated_data.pop('members')
        bank_account = validated_data.pop('bank_account')

        trip = Trip.objects.create(**validated_data)
        print(validated_data)
        for location_data in locations_data:
            Location.objects.create(trip=trip, **location_data)

        for member_data in members_data:
            username = member_data['user']['username']
            try:
                user = User.objects.get(username=username)
                Member.objects.create(trip=trip, user=user, bank_account=bank_account)
            except User.DoesNotExist:
                continue

        request_user = self.context['request'].user
        Member.objects.create(trip=trip, user=request_user, bank_account=bank_account)

        return trip
    
    def update(self, instance, validated_data):
        Location.objects.filter(trip=instance).delete()
        Member.objects.filter(trip=instance).delete()

        locations_data = validated_data.pop('locations')
        members_data = validated_data.pop('members')
        bank_account = validated_data.pop('bank_account')

        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.save()

        for location_data in locations_data:
            Location.objects.create(trip=instance, **location_data)

        for member_data in members_data:
            username = member_data['user']['username']
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
