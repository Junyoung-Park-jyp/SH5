from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username']

class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'user_key']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if User.objects.filter(email=validated_data['email']).exists():
            raise ValidationError("이미 존재하는 이메일 혹은 닉네임입니다.")
        user = User(
            username=validated_data['username'],
            email=validated_data['email'], 
            user_key=validated_data['user_key']
        )
        user.set_password(validated_data['password'])  # 비밀번호 해시
        user.save()
        return user
