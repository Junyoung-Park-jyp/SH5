from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()
        
        
class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'user_key']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'], 
            user_key = validated_data['user_key']
        )
        user.set_password(validated_data['password'])  # 비밀번호 해시
        user.save()
        return user