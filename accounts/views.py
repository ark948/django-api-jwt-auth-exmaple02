from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from accounts.serializers import UserRegisterSerializer, UserOTPSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import status
from accounts.utils import send_code_to_user
from accounts.models import OneTimePassword
from rest_framework.permissions import IsAuthenticated

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
        serializer = self.serializer_class(data=request.data, context={'request': request})
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