from django.urls import path
from knox.views import LogoutView, LogoutAllView

from .views import (
    RegisterView,
    SendOTPView,
    VerifyOTPLoginView,
    UpdateUserAPI,
    LoginView,
    GetCurrentUser,
)

urlpatterns = [
    # User registration
    path('register/', RegisterView.as_view(), name='register'),

    # User update (use dynamic pk for updating user)
    path('update-user/<int:pk>/', UpdateUserAPI.as_view(), name='update-user'),

    # Login and Logout
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout-all/', LogoutAllView.as_view(), name='logout-all'),

    # OTP related routes
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPLoginView.as_view(), name='verify-otp'),

    # Get current authenticated user info
    path('me/', GetCurrentUser.as_view(), name='get-current-user'),
]
