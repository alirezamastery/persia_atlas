import os
import subprocess
import base64
import uuid

from django.core.files.storage import default_storage
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser


class StreamVideoChunkView(APIView):

    # parser_classes = [MultiPartParser]

    def post(self, request):
        # file = request.FILES.get('file')
        # save_rel_path = f'stream/chunk/{file.name}'
        # saved_file = default_storage.save(save_rel_path, file)
        # save_complete_path = os.path.join(settings.MEDIA_ROOT, saved_Zfile)
        # print(f'{save_complete_path = }')

        chunk = request.data.get('chunk')
        save_complete_path = os.path.join(settings.MEDIA_ROOT, 'stream/chunk/', 'test.mp4')
        print(f'{save_complete_path = }')
        with open(save_complete_path, 'ab') as f:
            f.write(base64.b64decode(chunk))

        # command = [
        #     'ffmpeg', '-re', '-i', save_complete_path,
        #     '-vf', 'pad=ceil(iw/2)*2:ceil(ih/2)*2',  # handle input height and width to be compatible with libx264
        #     '-c:v', 'libx264', '-preset', 'veryfast', '-tune', 'zerolatency',
        #     '-c:a', 'aac', '-ar', '44100',
        #     '-f', 'flv',
        #     'rtmp://localhost/live/chaikin'
        # ]
        # subprocess.run(command)

        return Response({'info': 'ok'})


__all__ = [
    'StreamVideoChunkView'
]
