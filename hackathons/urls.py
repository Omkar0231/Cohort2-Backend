from django.urls import path
from .views import HackathonListView, HackathonDetailView, ApplyHackathonView

urlpatterns = [
    path('', HackathonListView.as_view(), name='hackathon-list'),
    path('<int:pk>/', HackathonDetailView.as_view(), name='hackathon-detail'),
    path('<int:pk>/apply/', ApplyHackathonView.as_view(), name='hackathon-apply'),
]