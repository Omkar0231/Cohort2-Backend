from django.urls import path
from .views import HackathonListView, HackathonDetailView, ApplyHackathonView

urlpatterns = [
    path('hackathons/', HackathonListView.as_view(), name='hackathon-list'),
    path('hackathons/<int:id>/', HackathonDetailView.as_view(), name='hackathon-detail'),
    path('hackathons/apply/', ApplyHackathonView.as_view(), name='hackathon-apply'),
]
