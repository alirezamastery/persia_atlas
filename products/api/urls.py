from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import (ProductVariantsViewSet, ProductVariantsListView, ActualProductListView, ActualProductDetailView)


urlpatterns = [
    path('variants/', ProductVariantsListView.as_view()),
    path('actual-products/', ActualProductListView.as_view()),
    path('actual-products/<int:pk>/', ActualProductDetailView.as_view()),
]

router = SimpleRouter()

router.register('variants', ProductVariantsViewSet)

# urlpatterns += router.urls
