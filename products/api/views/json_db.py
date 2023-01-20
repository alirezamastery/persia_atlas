from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from utils.json_db import jdb


class DigiLoginCredentialsView(APIView):

    def get(self, request):
        response = {
            jdb.keys.DIGI_USERNAME: jdb.get(jdb.keys.DIGI_USERNAME),
            jdb.keys.DIGI_PASSWORD: jdb.get(jdb.keys.DIGI_PASSWORD),
        }
        return Response(response)

    def post(self, request):
        username = request.data.get(jdb.keys.DIGI_USERNAME, jdb.get(jdb.keys.DIGI_USERNAME))
        password = request.data.get(jdb.keys.DIGI_PASSWORD, jdb.get(jdb.keys.DIGI_PASSWORD))
        jdb.set(jdb.keys.DIGI_USERNAME, username)
        jdb.set(jdb.keys.DIGI_PASSWORD, password)
        response = {
            jdb.keys.DIGI_USERNAME: username,
            jdb.keys.DIGI_PASSWORD: password,
        }
        return Response(response, status=status.HTTP_201_CREATED)


__all__ = [
    'DigiLoginCredentialsView',
]
