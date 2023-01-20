import requests

from django.contrib.auth import settings
from utils.logging import logger
from utils.json_db import jdb


class ServerSession:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.login_credentials = settings.DIGIKALA_LOGIN_CREDENTIALS
        self.login_credentials = {
            'login[email]':    jdb.get(jdb.keys.DIGI_USERNAME),
            'login[password]': jdb.get(jdb.keys.DIGI_PASSWORD),
        }
        self.session = requests.Session()

    def login(self):
        login_url = settings.DIGIKALA_URLS['login']
        response = self.session.post(login_url, data=self.login_credentials,
                                     timeout=10,
                                     headers={'user-agent': 'Mozilla/5.0'})
        logger(response, color='yellow')
        logger(f'{response.url = }', color='yellow')
        if response.url == login_url:
            raise Exception('could not login')
