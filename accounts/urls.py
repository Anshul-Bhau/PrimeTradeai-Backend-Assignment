from django.urls import path, include
from rest_framework_simplejwt.views import  TokenRefreshView
from .views import *
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='taken_refresh'),
    path('me/', MeView.as_view(), name='me')
]