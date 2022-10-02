import pickle
from pathlib import Path

import requests
from django.conf import settings
from rest_framework.exceptions import APIException
from rest_framework import status

from scripts.json_db import JsonDB
from utils.logging import logger, plogger


def get_variant_detail(dkpc: int) -> dict:
    pass


class DigikalaServerError(APIException):
    status_code = status.HTTP_418_IM_A_TEAPOT
    default_detail = 'Digikala server did not respond'


class DigikalaSession:
    COOKIE_FILE = 'session_cookies'
    TIMEOUT = 10
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'}

    def __init__(self):
        self.session = requests.Session()
        cookie_file = Path(f'./{self.COOKIE_FILE}')
        if cookie_file.is_file():
            # logger('loading cookies', color='yellow')
            with open('session_cookies', 'rb') as f:
                self.session.cookies.update(pickle.load(f))
        else:
            self.login()

    def login(self):
        logger('logging in', color='yellow')
        json_db = JsonDB()
        login_credentials = {
            'login[email]':    json_db.get(JsonDB.keys.DIGI_USERNAME),
            'login[password]': json_db.get(JsonDB.keys.DIGI_PASSWORD),
        }
        login_url = settings.DIGIKALA_URLS['login']
        response = self.session.post(login_url,
                                     data=login_credentials,
                                     timeout=10,
                                     headers=self.HEADERS)
        if response.url == login_url:
            raise DigikalaServerError({'login failed': 'Could not Login to Digikala, maybe password has changed'})
        logger('logged in', color='green')
        with open(f'./{self.COOKIE_FILE}', 'wb') as f:
            pickle.dump(self.session.cookies, f)

    def post(self, url, payload):
        try:
            response = self.session.post(url,
                                         data=payload,
                                         timeout=self.TIMEOUT,
                                         headers=self.HEADERS)
        except:
            raise DigikalaServerError()
        if 'account/login' in response.url:
            self.login()
            return self.post(url, payload)
        return response.json()

    def get(self, url):
        try:
            response = self.session.get(url,
                                        timeout=self.TIMEOUT,
                                        headers=self.HEADERS)
        except Exception as e:
            logger('DIGIKALA RESPONSE ERROR')
            logger(e)
            raise DigikalaServerError()
        if 'account/login' in response.url:
            self.login()
            return self.get(url)
        logger('response.url:', response.url)
        # plogger(response.content)
        try:
            return response.json()
        except:
            logger('DIGIKALA DECODE ERROR')
            plogger(response.content)
            raise DigikalaServerError()


digi_session = DigikalaSession()
