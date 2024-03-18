from typing import List
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from drf_spectacular.openapi import AutoSchema

from utils.drf.permissions import IsAdmin


__all__ = [
    'CustomAutoSchema',
    'CustomSpectacularAPIView',
    'CustomSpectacularRedocView',
    'CustomSpectacularSwaggerView',
]


class CustomAutoSchema(AutoSchema):

    def get_tags(self) -> List[str]:
        return ['okok']


class CustomSpectacularAPIView(SpectacularAPIView):
    permission_classes = [IsAdmin]


class CustomSpectacularRedocView(SpectacularRedocView):
    permission_classes = [IsAdmin]


class CustomSpectacularSwaggerView(SpectacularSwaggerView):
    permission_classes = [IsAdmin]
