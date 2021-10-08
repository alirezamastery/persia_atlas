import requests

from products.robot.core.robot_settings import LOGIN_CREDENTIALS, LOGIN_URL
from utils.logging import logger


class ServerSession:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.login_credentials = LOGIN_CREDENTIALS
        self.session = requests.Session()

    def login(self):
        response = self.session.post(LOGIN_URL, data=self.login_credentials, timeout=30)
        logger(response, color='yellow')
        logger(f'{response.url = }', color='yellow')
        if response.url == LOGIN_URL:
            raise Exception('could not login')
