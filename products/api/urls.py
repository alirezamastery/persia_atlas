from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import (UpdateVariantDigiDataView, UpdatePriceMinView, ActualProductViewSet,
                    BrandViewSet, ActualProductDigikalaDataView,
                    UpdateVariantStatusView, ProductVariantViewSet)


urlpatterns = [
    path('actual-product-variants/<int:pk>/', ActualProductDigikalaDataView.as_view()),
    path('update-variant-data/', UpdateVariantDigiDataView.as_view()),
    path('update-variant-status/', UpdateVariantStatusView.as_view()),
    path('update-variant-price-min/', UpdatePriceMinView.as_view()),
]

router = SimpleRouter()

router.register('brands', BrandViewSet)
router.register('actual-products', ActualProductViewSet)
router.register('variants', ProductVariantViewSet)

urlpatterns += router.urls
