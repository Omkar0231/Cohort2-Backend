from django.contrib.auth import login
from knox.models import AuthToken
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from knox.views import LoginView as KnoxLoginView
from rest_framework.views import APIView
from .serializers import  OTPVerifySerializer
from .models import CustomUser
from .serializers import( CreateUserSerializer, UpdateUserSerializer,
LoginSerializer, OTPVerifySerializer)
from .utils import send_otp_to_email


# User Registration API
class CreateUserAPI(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)


# User Update  API
class UpdateUserAPI(UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UpdateUserSerializer


# Email/Password Login Using Knox token
class LoginAPIView(KnoxLoginView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super().post(request, format=None)

#Send OTP to eamil

class SendOTPView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        user_exists = CustomUser.objects.filter(email=email).exists()
        if not user_exists:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        send_otp_to_email(email)
        return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)

#Verify otp and login

class VerifyOTPLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            token =AuthToken.objects.create(user)[1]
            return Response({
                "token": token,
                "user":{
                    "id":user.id,
                    "email":user.email,
                    "first_name":user.first_name,
                    "last_name":user.last_name,
                    "gender":user.gender,
                }
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)