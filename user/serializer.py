import re
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.serializers import ModelSerializer
from rest_framework import status
from rest_framework import exceptions, serializers
from django.contrib.auth.hashers import check_password
from user.models import User

class UserSignUpSerializer(ModelSerializer):
    def create(self, validated_data):
        password = validated_data.get('password')

        password_regexp = '^(?=.*[\d])((?=.*[a-z])|(?=.*[A-Z]))[\w\d!@#$%^&*()]{8,20}$'

        if not re.match(password_regexp, password):
            raise serializers.ValidationError({"password": ["영문자/숫자를 포함하여 8자 이상의 패스워드로 설정해주세요."]})

        user = User.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}



class UserSignInSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def user_signin(self, data):
        user = User.objects.get(email=data['email'])
        if not user or not check_password(data['password'], user.password):
            raise_exception = exceptions.APIException(detail="failed signin")
            raise_exception.status_code = status.HTTP_400_BAD_REQUEST
            raise raise_exception

        refresh = super().get_token(user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)
        data = {'user_info': str(user), 'refresh': refresh_token, 'access': access_token}

        return data