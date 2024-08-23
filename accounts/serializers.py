from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from accounts.models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

class UserRegisterSerializer(ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')
        if password != password2:
            raise serializers.ValidationError("passwords do not match")
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            first_name = validated_data.get('first_name'),
            last_name = validated_data.get('last_name'),
            password = validated_data.get('password'),
        )
        return user
    
class UserOTPSerializer(Serializer):
    otp = serializers.IntegerField(max_value=999999, min_value=100000, required=True)


class LoginSerializer(ModelSerializer):
    # only email and password will be requested from user
    # since they don't have read_only
    email = serializers.EmailField(max_length=225, min_length=6)
    password = serializers.CharField(max_length=68, write_only=True)
    # password has write_only, because we don't want it returned with response (probably)
    full_name = serializers.CharField(max_length=225, read_only=True)
    access_token = serializers.CharField(max_length=225, read_only=True)
    refresh_token = serializers.CharField(max_length=225, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'full_name', 'access_token', 'refresh_token']

    def validate(self, attrs):
        # customizing the validate method of Model serializer
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        # get the request object, since we will need it for authentication
        user = authenticate(request, email=email, password=password)
        # if authenticate run with no problem, it will return the user object
        if not user:
            # if not user was returned, credentials was not valid
            raise AuthenticationFailed("invalid credentials, try again.")
        if not user.is_verified:
            # user can be returned, but it may not have been verified
            raise AuthenticationFailed("email is not verified.")
        user_tokens = user.tokens()
        # get access and refresh token from tokens method of custom user model
        
        return {
            'email': user.email,
            'full_name': user.get_full_name,
            'access_token': str(user_tokens.get('access')),
            'refresh_token': str(user_tokens.get('refresh')),
        }