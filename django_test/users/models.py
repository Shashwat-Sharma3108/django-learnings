from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from datetime import timedelta  # Import timedelta to handle OTP expiry

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)  # Add the OTP creation time
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    # ... (rest of the model code)

    def generate_otp(self):
        import random
        from django.utils import timezone

        otp = str(random.randint(100000, 999999))
        self.otp = otp
        self.otp_created_at = timezone.now()  # Set the OTP creation time
        self.save()
        return otp

    def is_otp_expired(self):
        if self.otp_created_at:
            return timezone.now() - self.otp_created_at > timedelta(minutes=10)
        return True

    def __str__(self):
        return self.email
