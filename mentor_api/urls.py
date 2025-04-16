from django.contrib import admin
from django.urls import path, include
from accounts.views import home_view, RegisterView, LoginView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Core API Endpoints
    path('', home_view, name='home'),  # Root welcome message
    path('register/', RegisterView.as_view(), name='register'),

    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),

    # App-specific URLs
    path('accounts/', include('accounts.urls')),
    path('api/hackathons/', include('hackathons.urls')),
]
