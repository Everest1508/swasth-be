from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'phone', 'role', 'first_name', 'last_name')
        extra_kwargs = {
            'email': {'required': True},
            'phone': {'required': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'role', 'first_name', 'last_name', 'is_verified', 'created_at')
        read_only_fields = ('id', 'created_at', 'is_verified')


class OTPLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    otp = serializers.CharField(max_length=6, required=True)


class OTPRequestSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)

