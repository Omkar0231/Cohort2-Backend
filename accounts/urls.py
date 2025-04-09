from django.urls import path
from . import views
from knox.views import LogoutView,LogoutAllView

from .views import SendOTPView, VerifyOTPLoginView

urlpatterns = [
    path('create-user/', views.CreateUserAPI.as_view()),
    path('update-user/<int:pk>/', views.UpdateUserAPI.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('logout-all/', LogoutAllView.as_view()),


    path('send-otp/',SendOTPView.as_view(),name='send-otp'),
    path('verify-otp/', VerifyOTPLoginView.as_view(), name='verify-otp'),
]
