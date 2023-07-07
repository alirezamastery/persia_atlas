import uuid

from django.core.files.storage import default_storage
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from ..filters import *
from shop.models import *
from shop.serializers import *
from utils.drf.permissions import *


__all__ = [
    'ImageViewSet',
]


class ImageViewSet(ModelViewSet):
    queryset = ProductImage.objects.all().order_by('id')
    serializer_class = ImageReadSerializer
    permission_classes = [IsAdmin]

    @action(methods=['POST'], detail=False, url_path='upload')
    def upload(self, request, *args, **kwargs):
        file = request.FILES.get('image')
        parts = file.name.split('.')
        print('==============', file)
        if len(parts) == 0:
            return Response({'error': 'no file extension'}, status=400)
        extension = parts[-1]
        if extension not in ['jpg', 'JPEG', 'jpeg', 'png']:
            return Response({'error': 'unacceptable file format for image'}, status=400)

        new_name = f'{uuid.uuid4().hex}.{extension}'
        path = f'units/images/{new_name}'
        saved_file = default_storage.save(path, file)
        file_url = default_storage.url(saved_file)
        # if file_url.startswith('/media/'):
        #     file_url = file_url[7:]
        response = {
            'file_address': file_url
        }
        return Response(response)
