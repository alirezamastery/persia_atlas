from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *


app_name = 'shop_api'

router = DefaultRouter()

urlpatterns = [
]

router.register('brands', BrandViewSet, basename='brands')
router.register('categories', CategoryViewSet, basename='categories')
router.register('categories-admin', CategoryAdminViewset, basename='categories_admin')
router.register('product-attrs', ProductAttributeViewSet, basename='product-attrs')
router.register('products', ProductViewSet, basename='products')
router.register('variants', ProductVariantViewSet, basename='variants')
router.register('selector-types', VariantSelectorTypeViewSet, basename='selector_types')
router.register('orders', OrderViewSet, basename='orders')

urlpatterns += router.urls
