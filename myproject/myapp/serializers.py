from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  # 비밀번호는 읽을 수 없도록 설정
        }

    def create(self, validated_data):
        """
        사용자 생성 시 비밀번호를 해시 처리
        """
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
