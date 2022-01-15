from rest_framework.routers import DefaultRouter

from .views import CostViewSet, CostTypeViewSet


router = DefaultRouter()

urlpatterns = []

router.register('costs', CostViewSet)
router.register('cost-types', CostTypeViewSet)

urlpatterns += router.urls
