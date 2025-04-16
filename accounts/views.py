from django.http import JsonResponse
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from knox.models import AuthToken

from .models import CustomUser, EmailOTP
from .serializers import (
    UserSerializer,
    CreateUserSerializer,
    UpdateUserSerializer,
    LoginSerializer,
)


# -------------------------------
# Home View
# -------------------------------
def home_view(request):
    """Welcome message for root endpoint."""
    return JsonResponse({"message": "Welcome to the Mentor Dashboard API!"})


# -------------------------------
# OTP: Send OTP to Email
# -------------------------------
class SendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        from .otp_utils import send_otp_to_email
        send_otp_to_email(email)
        return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)


# -------------------------------
# OTP: Verify OTP and Login
# -------------------------------
class VerifyOTPLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        if not email or not otp:
            return Response({"error": "Email and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            email_otp = EmailOTP.objects.filter(email=email).latest('id')
        except EmailOTP.DoesNotExist:
            return Response({"error": "No OTP found."}, status=status.HTTP_404_NOT_FOUND)

        if email_otp.otp != otp:
            return Response({"error": "OTP does not match."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        _, token = AuthToken.objects.create(user)
        return Response({
            "token": token,
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)


# -------------------------------
# Traditional Login (Email + Password)
# -------------------------------
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        _, token = AuthToken.objects.create(user)
        return Response({
            'token': token,
            'user': UserSerializer(user).data
        })


# -------------------------------
# Register New User
# -------------------------------
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = [AllowAny]


# -------------------------------
# Update Existing User
# -------------------------------
class UpdateUserAPI(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated]


# -------------------------------
# Get Current User Info
# -------------------------------
class GetCurrentUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
