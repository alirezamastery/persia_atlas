from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.api.admin.views import *


app_name = 'users_admin'

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileViewAdmin.as_view(), name='user-profile')
]

router = DefaultRouter()

router.register('users', UserViewSetAdmin)
router.register('auth-groups', AuthGroupViewSetAdmin)
router.register('auth-permissions', AuthPermissionViewSetAdmin)

urlpatterns += router.urls
