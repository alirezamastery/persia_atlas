from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *


app_name = 'users'

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='user_profile')
]

router = DefaultRouter()

router.register('users', UserViewSet)

urlpatterns += router.urls
