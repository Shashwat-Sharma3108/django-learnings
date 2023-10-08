from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer
from .models import CustomUser
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

import random

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create the user
        user = serializer.save()

        return Response({'message': 'User registered successfully.'}, status=status.HTTP_201_CREATED)

class UserLoginView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def create(self, request):
        user_form_data = request.data
        username = user_form_data['username']
        password = user_form_data['password']

        try:
            user = CustomUser.objects.get(email=username)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        if password == user.password:
            self.send_otp_email(user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            # You can customize the response message or token generation here
            response_data = {
                'detail': 'Login successful.',
                'access_token': access_token,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid Username or Password.'}, status=status.HTTP_404_NOT_FOUND)


    def send_otp_email(self, user):
        otp = str(random.randint(100000, 999999))
        user.otp = otp
        user.otp_created_at = timezone.now()
        user.save()

        subject = 'Your OTP for Login'
        message = f'Your OTP for login is {otp}. It is valid for 10 minutes.'
        from_email = 'your_email@example.com'  # Replace with your email
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

class UserOTPVerificatiomView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        otp = request.GET.get('otp')
        username = request.user.username

        user = CustomUser.objects.get(email=username)
        otp = user.otp
        if otp == user.otp:
            if user.is_otp_expired():
                return Response({'detail': 'OTP Verified'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Token Expired'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'detail': 'Invalid OTP'}, status=status.HTTP_404_NOT_FOUND)