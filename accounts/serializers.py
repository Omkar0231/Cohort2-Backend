from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'gender', 'role']


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'gender', 'role', 'phone', 'profile_picture', 'password']
        extra_kwargs = {
            'password': {'required': True, 'write_only': True},
        }

    def validate(self, attrs):
        email = attrs.get('email', '').strip().lower()
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Email already registered'})
        attrs['email'] = email  # normalize email
        return attrs

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'gender', 'role', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email', '').strip().lower()
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError({'detail': 'Email and password are required.'})

        user = authenticate(request=self.context.get('request'), username=email, password=password)

        if not user:
            raise serializers.ValidationError({'detail': 'Invalid email or password.'})

        attrs['user'] = user
        return attrs


class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = attrs.get('email').strip().lower()
        otp = attrs.get('otp')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({'email': 'Email does not exist'})

        if not user.is_otp_valid(otp):
            raise serializers.ValidationError({'otp': 'OTP is invalid or expired'})

        attrs['user'] = user
        return attrs
