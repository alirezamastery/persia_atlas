from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import (ProductVariantsListView, UpdateVariantDigiDataView, UpdatePriceMinView,
                    ActualProductViewSet, ProductVariantDigikalaDataView, ActualProductDigikalaDataView,
                    UpdateVariantStatusView)


urlpatterns = [
    path('variants/', ProductVariantsListView.as_view()),
    path('variant-group/', ProductVariantDigikalaDataView.as_view()),

    path('actual-product-variants/<int:pk>/', ActualProductDigikalaDataView.as_view()),
    path('update-variant-data/', UpdateVariantDigiDataView.as_view()),
    path('update-variant-status/', UpdateVariantStatusView.as_view()),
    path('update-variant-price-min/', UpdatePriceMinView.as_view()),

]

router = SimpleRouter()

# router.register('variants', ProductVariantsViewSet)
router.register('actual-products', ActualProductViewSet)

urlpatterns += router.urls
