import json
from typing import Optional
from jwt import decode as jwt_decode

from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from utils.logging import logger


class TokenAuthMiddleware(BaseMiddleware):

    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        token = await self.extract_credentials(scope)

        scope['user'] = await self.authenticate(token)
        scope['token'] = token

        return await super().__call__(scope, receive, send)

    @staticmethod
    async def extract_credentials(scope):
        headers = scope['headers']
        headers = {h[0]: h[1] for h in headers}
        token = None
        web_token = headers.get(b'sec-websocket-protocol')
        if web_token:
            raw_data = headers[b'sec-websocket-protocol'].decode('ascii')
            token = raw_data
            try:
                data = json.loads(raw_data)
            except json.decoder.JSONDecodeError:
                data = raw_data
            if isinstance(data, list):
                token = data[0]
            elif isinstance(data, str):
                token = data
            else:
                # logger('wrong token type')
                pass
        else:
            try:
                token = headers[b'token'].decode()
            except Exception as e:
                logger('ERROR:', e, color='red')
        return token

    @staticmethod
    @database_sync_to_async
    def authenticate(token: Optional[str]):
        if token is None:
            return AnonymousUser()
        try:
            # This will automatically validate the token and raise an error if token is invalid
            UntypedToken(token)
        except (InvalidToken, TokenError) as e:
            # Token is invalid
            logger(e)
            return AnonymousUser()

        algorithm = settings.SIMPLE_JWT['ALGORITHM']
        user_id_claim = settings.SIMPLE_JWT['USER_ID_CLAIM']

        decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=[algorithm])
        return get_user_model().objects.get(id=decoded_data[user_id_claim])
