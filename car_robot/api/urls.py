from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()

urlpatterns = [
]

router.register('cars', CarViewSet)

urlpatterns += router.urls
