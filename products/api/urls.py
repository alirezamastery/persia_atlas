from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import *


urlpatterns = [
    path('actual-product-variants/<int:pk>/', ActualProductDigikalaDataView.as_view()),
    path('update-variant-data/', UpdateVariantDigiDataView.as_view()),
    path('update-variant-status/', UpdateVariantStatusView.as_view()),
    path('update-variant-price-min/', UpdatePriceMinView.as_view()),
    path('invoice-excel/', InvoiceExcelView.as_view()),
    path('file-test/', FileDownloadTest.as_view()),
]

router = SimpleRouter()

router.register('brands', BrandViewSet)
router.register('actual-products', ActualProductViewSet)
router.register('products', ProductViewSet)
router.register('products-types', ProductTypeViewSet)
router.register('product-type-selectors', ProductTypeSelectorViewSet)
router.register('product-type-selector-values', ProductTypeSelectorValueViewSet)
router.register('variants', ProductVariantViewSet)

router.register('invoices', InvoiceViewSet)
router.register('invoice-items', InvoiceItemViewSet)

urlpatterns += router.urls
