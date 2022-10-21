from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import *


urlpatterns = [
    path('variant-digi-data/<int:pk>/', VariantDigiDataView.as_view()),
    path('variant-digi-data-dkpc/<int:dkpc>/', VariantDigiDataDKPCView.as_view()),
    path('update-variant-data/<int:dkpc>/', UpdateVariantDigiDataView.as_view()),
    path('digi-creds/', DigiLoginCredentialsView.as_view()),
    path('scrape-invoice-page/', ScrapeInvoiceView.as_view()),
    path('task-state/<str:task_id>/', CeleryTaskStateView.as_view(), name='task_status'),
    path('brands-all/', BrandListView.as_view()),
    path('actual-product-by-brand/<int:brand_id>/', ActualProductByBrandView.as_view()),
    path('inactive-variants/', InactiveVariantsView.as_view()),
    path('robot-status/', RobotStatusView.as_view()),

    # for testing purposes:
    path('file-test/', FileDownloadTest.as_view()),
    path('task-test-success/', TestCelerySuccessTask.as_view()),
    path('task-test-fail/', TestCeleryFailTask.as_view()),
]

router = SimpleRouter()

router.register('brands', BrandViewSet)
router.register('actual-products', ActualProductViewSet)
router.register('products', ProductViewSet)
router.register('products-types', ProductTypeViewSet)
router.register('variant-selector-types', VariantSelectorTypeViewSet)
router.register('variant-selectors', VariantSelectorViewSet)
router.register('variants', ProductVariantViewSet)

urlpatterns += router.urls
