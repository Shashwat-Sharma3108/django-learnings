from django.urls import path
from .views import UserRegistrationView,UserLoginView,UserOTPVerificatiomView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('otp-verificatiopn/', UserOTPVerificatiomView.as_view(), name='user-otp-verification'),
]
