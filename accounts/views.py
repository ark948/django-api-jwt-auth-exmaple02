from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from accounts.serializers import (
    UserRegisterSerializer,
    UserOTPSerializer,
    LoginSerializer,
    PasswordResetRequestSerializer,
    SetNewPasswordSerializer,
    LogoutUserSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from accounts.utils import send_code_to_user
from accounts.models import OneTimePassword, User
from rest_framework.permissions import IsAuthenticated
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Create your views here.


class RegisterUserView(GenericAPIView):
    serializer_class = UserRegisterSerializer
    # get data from request, validate it, if valid, create and return user object

    def post(self, request):
        # customizing the POST request of GenericAPIView
        user_data = request.data
        # get user data from request object
        serializer = self.serializer_class(data=user_data)
        # get the serilizer object filled with user data, which is UserRegisterSerializer
        if serializer.is_valid(raise_exception=True):
            # run its validation, if ok, continue
            serializer.save()
            # and save it
            user = serializer.data
            # the returned data will be a newly created user object
            send_code_to_user(user['email'])
            return Response({
                'data': user,
                'message': f'Hi, thanks for signing up. please check your email.',
            }, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # if validation of serializer with data failed, return 400 error


class VerifyUserEmail(GenericAPIView):
    # write a serializer for OTP
    serializer_class = UserOTPSerializer

    def post(self, request):
        # customizing the POST request
        otpcode = request.data.get('otp')
        # get the otp from request object
        try:
            user_code_obj = OneTimePassword.objects.get(code=otpcode)
            # check the otp database table for it, if exits, otp was valid
            user = user_code_obj.user
            # if found, get the related user from it
            if not user.is_verified:
                # check if that user is verified
                user.is_verified = True
                # if it is not, verify it since the otp was valid
                user.save()
                # save changes for user object
                return Response({
                    'message': 'account email verified successfully',
                }, status=status.HTTP_200_OK)
            return Response({
                'message': 'code is invalid or user is already verified.'
            }, status=status.HTTP_204_NO_CONTENT)
            # if user was verified, or otp was not found in otp database table
            # return error
        except OneTimePassword.DoesNotExist:
            return Response({'message': 'passcode not provided'}, status=status.HTTP_404_NOT_FOUND)


class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        # customizing the POST request
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        # get the serializer object with data feeded
        serializer.is_valid(raise_exception=True)
        # run it here, if it was valid
        # it will return a dict containing user email, full name, refresh and access token
        return Response(serializer.data, status=status.HTTP_200_OK)
        # send it back to user with status code of ok


class TestAuthenticationView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {
            'msg': 'it works.'
        }
        return Response(data, status=status.HTTP_200_OK)


class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    # just accepts an email from user
    # if that email exists in database i.e. a user has registered using that email
    # generate an encoded string containing that user's id
    # and a token

    def post(self, request):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({
            'message': 'A link containing password reset link has been sent to you.'
        }, status=status.HTTP_200_OK)


class PasswordResetConfirmView(GenericAPIView):
    # used to provide uidb64 and token for user to aquire
    # and send along to (SetNewPasswordView) to set a new password
    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({
                    'message': "Token is invalid or has expired"
                }, status=status.HTTP_401_UNAUTHORIZED)
            return Response({
                'success': True,
                'message': 'Credentials is valid',
                'uidb64': uidb64,
                'token': token
            }, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError:
            return Response({
                'message': "Token is invalid or has expired"
            }, status=status.HTTP_401_UNAUTHORIZED)
        

class SetNewPasswordView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({
            'message': 'Password reset successful.'
        }, status=status.HTTP_200_OK)
    
class LogoutUserView(GenericAPIView):
    serializer_class = LogoutUserSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)