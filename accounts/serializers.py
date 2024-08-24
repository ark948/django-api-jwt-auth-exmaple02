from django.urls import reverse
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from accounts.models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from accounts.utils import send_normal_email

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
    

class PasswordResetRequestSerializer(Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            request = self.context.get('request')
            site_domain = get_current_site(request).domain
            relative_link = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            abslink = f'http://{site_domain}{relative_link}'
            email_body = f'Hello, Please use the following link to reset your password \n {abslink}'
            data = {
                'email_body': email_body,
                'email_subject': "Reset your password.",
                'to_email': user.email
            }
            send_normal_email(data)
        else:
            raise serializers.ValidationError("User was not found.")
        return super().validate(attrs)
    

class SetNewPasswordSerializer(Serializer):
    password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    confirm_password = serializers.CharField(max_length=100, min_length=6, write_only=True)
    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    class Meta:
        fields = ['password', 'confirm_password', 'uidb64', 'token']

    def validate(self, attrs):
        try:
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            password = attrs.get('password')
            confirm_password=attrs.get('confirm_password')

            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('Reset link is invalid or has expired.', 401)
            if password != confirm_password:
                raise AuthenticationFailed('Passwords do not match.')
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            return AuthenticationFailed('Link is invalid or has expired.')