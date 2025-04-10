from django.urls import path
from knox.views import LogoutView, LogoutAllView
from .views import (
    SendOTPView, VerifyOTPLoginView,
    CreateUserAPI, UpdateUserAPI,
    LoginAPIView,GetCurrentUser
)

urlpatterns = [
    path('create-user/', CreateUserAPI.as_view(), name='create-user'),
    path('update-user/<int:pk>/', UpdateUserAPI.as_view(), name='update-user'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout-all/', LogoutAllView.as_view(), name='logout-all'),
    path('send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('verify-otp/', VerifyOTPLoginView.as_view(), name='verify-otp'),

    path('me/', GetCurrentUser.as_view(), name='get-current-user'),

]
