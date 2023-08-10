from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *


app_name = 'shop_api'

router = DefaultRouter()

urlpatterns = [
]


router.register('categories-admin', CategoryViewsetAdmin, basename='categories-admin')
router.register('categories', CategoryViewSetPublic, basename='categories')

router.register('products-admin', ProductViewSetAdmin, basename='products-admin')
router.register('products', ProductViewSetPublic, basename='products')

router.register('brands', BrandViewSet, basename='brands')
router.register('product-attrs', ProductAttributeViewSet, basename='product-attrs')
router.register('selector-types', VariantSelectorTypeViewSet, basename='selector_types')
router.register('variants', ProductVariantViewSet, basename='variants')
router.register('images', ImageViewSet, basename='images')
router.register('orders', OrderViewSet, basename='orders')

urlpatterns += router.urls
