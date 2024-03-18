from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


urlpatterns_main = [
    path('admin/', admin.site.urls),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # path('api/users/', include('users.api.urls')),
    path('api/users/', include('users.api.admin.urls')),
    path('api/products/', include('products.api.urls')),
    path('api/accounting/', include('accounting.api.urls')),
    path('api/car-robot/', include('car_robot.api.urls')),
]

schema_view = get_schema_view(
    openapi.Info(
        title='Snippets API',
        default_version='v1',
        description='Test description',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='contact@snippets.local'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated,),
    patterns=urlpatterns_main
)

urlpatterns = urlpatterns_main + [
    # drf-yasg:
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
