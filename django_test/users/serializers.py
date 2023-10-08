from rest_framework import serializers
from .models import CustomUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'otp', 'otp_created_at')
        extra_kwargs = {
            'otp': {'write_only': True},  # Don't include OTP in the response
            'otp_created_at': {'write_only': True},  # Don't include OTP creation time in the response
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password:
            instance.set_password(password)
            
        instance.save()
        return instance
