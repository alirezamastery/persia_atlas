from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import ProductVariantsViewSet, ProductVariantsListView


urlpatterns = [
    path('vv/', ProductVariantsListView.as_view())
]

router = SimpleRouter()

router.register('variants', ProductVariantsViewSet)

# urlpatterns += router.urls
