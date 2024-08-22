from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Trip, Member


User = get_user_model()

class MemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Member
        fields = ['username', 'budget', 'bank_account']


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'
        
        
class TripDetailSerializer(serializers.ModelSerializer):
    members = MemberSerializer(source='member_set', many=True, read_only=True)
    class Meta:
        model = Trip
        fields = '__all__'
        
        
class MemberCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'
        
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']