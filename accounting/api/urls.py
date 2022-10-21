from django.urls import path
from rest_framework.routers import DefaultRouter

from .views.cost import *
from .views.income import *
from .views.invoice import *
from .views.profit import *


router = DefaultRouter()

urlpatterns = [
    path('profit/', ProfitView.as_view(), name='profit'),
    path('profit-year/', YearProfitView.as_view(), name='profit'),
]

router.register('costs', CostViewSet)
router.register('cost-types', CostTypeViewSet)
router.register('incomes', IncomeViewSet)
router.register('product-costs', ProductCostViewSet)
router.register('invoices', InvoiceViewSet)
router.register('invoice-items', InvoiceItemViewSet)

urlpatterns += router.urls
