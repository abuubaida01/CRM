from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from profiles.models import Profile
from user.models import User 
from .forms import UserChangeForm
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail

import logging
import os
from django.conf import settings
from decouple import config
from django.core.mail import EmailMessage
from django.utils.log import AdminEmailHandler
logger = logging.getLogger(__name__)

from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from user.serializers import SendPasswordResetEmailSerializer, UserChangePasswordSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserRegistrationSerializer, listUserSerializer,ChangeUserDetailSerializer
from django.contrib.auth import authenticate
from user.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework import generics

from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from .models import EmailVerificationToken

from django.core.mail import send_mail
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.throttling import UserRateThrottle
from rest_framework.parsers import JSONParser
from django.shortcuts import reverse  # Import reverse to generate the registration URL

INFO_EMAIL = config('INFO_EMAIL', cast=str, default='famior01@gmail.com')


# Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class OncePerDayUserThrottle(UserRateThrottle):
    rate = '5/day'

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny] 
    # throttle_classes = [OncePerDayUserThrottle] 
    #https://www.django-rest-framework.org/api-guide/throttling/
    parser_classes = [JSONParser]
    # https://www.django-rest-framework.org/api-guide/parsers/

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Send an email with the verification link
        link = send_verification_email(request, user)

        return Response({'msg': 'Registration Successful. Please check your email for verification instructions.', "click here": link}, status=status.HTTP_201_CREATED)

def send_verification_email(request, user):
    # Generate an email verification token
    # token = Token.objects.get_or_create(user=user)
    
    token = PasswordResetTokenGenerator().make_token(user)
    
    EmailVerificationToken.objects.get_or_create(user=user, token=token)
    
    link = f'http://localhost:8000/user/verify/{token}/'  # Access the token part of the tuple

    subject = 'Email Verification'
    message = f'Click the following link to verify your email: {link}'
    from_email = f"{INFO_EMAIL}"
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)
    return link

class VerifyEmailView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [AllowAny] 

    def get(self, request, token):
        try:
            email_token = EmailVerificationToken.objects.get(token=token)
            user = email_token.user

            # Mark the email as verified
            user.email_verified = True
            user.save()

            # Delete the email verification token
            email_token.delete()

            registration_url = reverse('user:login')  

            return Response({'msg': 'Email verified successfully.', 'Login here': registration_url}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'error': 'Email verification token does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [UserRenderer]
    # throttle_classes = [OncePerDayUserThrottle] 

    def get_queryset(self):
        return User.objects.none()

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            if user.email_verified:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'msg': 'Login Success'}, status=status.HTTP_200_OK)
            else:
                # Email not verified, create verification email
                verifyemail =   send_verification_email(self.request, user)
                print("\nverification token:\t", verifyemail)
                return Response({'msg': 'Email is not verified.', 'Verify your email here': verifyemail}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'errors': {'non_field_errors': ['Email or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)

class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

class SendPasswordResetEmailView(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)

class UserPasswordResetView(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view
    renderer_classes = [UserRenderer]
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)

class ChangeUserDetailView(generics.UpdateAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def put(self, request):
        # Retrieve the user instance using the get_object method
        user = self.get_object()
        serializer = ChangeUserDetailSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class listUserDetailsApi(generics.ListAPIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    serializer_class = listUserSerializer

    def get_queryset(self):
        # Return a queryset containing only the current user
        return User.objects.filter(username=self.request.user.username)
        


class DeleteUserAPI(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = self.request.user

        password = request.data.get('password')
        password2 = request.data.get('password2')

        if password != password2:
            return Response({"error": "Password and Confirm Password don't match"}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password):
            return Response({"error": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)

        # if password is correct, delete the user.
        user.delete()
        return Response({"Success":"User has been deleted"}, status=status.HTTP_200_OK)


        
# Configure logging globally
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'simple',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
    'formatters': {
        'console': {
            'format': '{levelname} {asctime:s} {name} {module} {filename} {lineno:d} {funcName} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime:s} {name} {module} {filename} {lineno:d} {funcName} {message}',
            'style': '{',
        },
    },
}

# # Error handlers
# def handler404(request, exception):
#     logger = logging.getLogger('django.request')
#     # don't send email for 404 errors
#     # logger.error('Page not found: %s', request.path, exc_info=exception)
#     return render(request, 'user/404.html')

# def handler500(request):
#     logger = logging.getLogger('django.request')
#     logger.error('Internal Server Error: %s', request.path, exc_info=True)
#     return render(request, 'user/500.html')

# def handler502(request):
#     logger = logging.getLogger('django.request')
#     logger.error('Bad Gateway: %s', request.path, exc_info=True)
#     return render(request, 'user/502.html')

# def handler503(request):
    # logger = logging.getLogger('django.request')
    # logger.error('Service Unavailable: %s', request.path, exc_info=True)
    # return render(request, 'user/503.html')