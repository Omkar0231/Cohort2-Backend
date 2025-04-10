from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields =('id','email','first_name','last_name','gender')
        extra_kwargs = {
            'password': {'write_only': True},
        }

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'required': True, 'write_only': True},
        }

    def validate(self, attrs):
        email =attrs.get('email', '').strip().lower()
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email already registered')
        return attrs

    def create(self,validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields =('id','email','first_name','last_name','gender')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }

    def update(self,instance, validated_data):
        password=validated_data.pop('password',None)
        if password:
            instance.set_password(password)
        return super().update(instance,validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'},trim_whitespace=False)

    def validate(self, attrs):
        email=attrs.get('email').lower()
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError('Email and password are required.')

        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email does not exist')
        user = authenticate(request=self.context.get('request'),email=email,password=password)

        if not user:
            raise serializers.ValidationError('User not found')

        attrs['user']=user
        return attrs

class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self,attrs):
        email=attrs.get('email')
        otp=attrs.get('otp')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('Email does not exist')

        if not user.is_otp_valid(otp):
            raise serializers.ValidationError('OTP does not match')
        attrs['user']=user
        return attrs