from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from utils.json_db import JsonDB


class DigiLoginCredentialsView(APIView):

    def get(self, request):
        db = JsonDB()
        response = {
            JsonDB.keys.DIGI_USERNAME: db.get(JsonDB.keys.DIGI_USERNAME),
            JsonDB.keys.DIGI_PASSWORD: db.get(JsonDB.keys.DIGI_PASSWORD),
        }
        return Response(response)

    def post(self, request):
        db = JsonDB()
        username = request.data.get(JsonDB.keys.DIGI_USERNAME, db.get(JsonDB.keys.DIGI_USERNAME))
        password = request.data.get(JsonDB.keys.DIGI_PASSWORD, db.get(JsonDB.keys.DIGI_PASSWORD))
        db.set(JsonDB.keys.DIGI_USERNAME, username)
        db.set(JsonDB.keys.DIGI_PASSWORD, password)
        response = {
            JsonDB.keys.DIGI_USERNAME: username,
            JsonDB.keys.DIGI_PASSWORD: password,
        }
        return Response(response, status=status.HTTP_201_CREATED)


__all__ = [
    'DigiLoginCredentialsView',
]
