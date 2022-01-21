from rest_framework.routers import DefaultRouter

from .views import *


router = DefaultRouter()

urlpatterns = []

router.register('costs', CostViewSet)
router.register('cost-types', CostTypeViewSet)
router.register('incomes', IncomeViewSet)
router.register('product-costs', ProductCostViewSet)

urlpatterns += router.urls
