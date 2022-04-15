import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from .utils import get_user_groupname
from .command_map import COMMAND_MAP
from .exceptions import InvalidClientPayload
from .constants import *
from utils.logging import logger, plogger, LOG_VALUE_WIDTH


class RobotConsumer(WebsocketConsumer):

    def connect(self):
        self.headers = dict(self.scope['headers'])
        # plogger(self.headers)
        self.user = self.scope['user']
        if self.user.is_authenticated:
            self.client_setup()
            self.accept(subprotocol=self.scope['token'])
        else:
            self.close()

    def client_setup(self):
        self.group_name = get_user_groupname(self.user.mobile)
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        async_to_sync(self.channel_layer.group_add)(
            ALL_USERS_GROUP,
            self.channel_name
        )
        self.commands = {
            cmd: Command(self.user, self.group_name) for cmd, Command in COMMAND_MAP.items()
        }

    def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name
            )

    def receive(self, text_data=None, bytes_data=None):
        try:
            plogger(json.loads(text_data), color='green')
        except:
            plogger(text_data, color='red')
        if not text_data:
            return

        request = json.loads(text_data)
        response = self.process_request_data(request)
        if response:
            self.send_to_client(response)

    def process_request_data(self, request: dict):
        command = request.get('command')
        req_key = request.get('req_key')

        if command in self.commands:
            try:
                response = self.commands[command].respond(request.get('payload'))
            except InvalidClientPayload as e:
                response = self.create_client_error(str(e))

        else:
            response = self.create_client_error(f'invalid command: {command}')

        if response.get(USER_RESPONSE) is not None:
            response[USER_RESPONSE]['req_key'] = req_key

        return response

    def create_client_error(self, error_msg: str):
        logger(error_msg, color='red')
        return {
            USER_CHANNEL:  get_user_groupname(user_id=self.user.mobile),
            USER_RESPONSE: {
                'type': 'error',
                'data': error_msg
            }
        }

    def send_to_client(self, response: dict):
        if response.get(USER_CHANNEL):
            self.direct_message(response[USER_CHANNEL], response[USER_RESPONSE])

        if others_channel := response.get(OTHERS_CHANNEL):
            logger(f'Other Receiver(s): {others_channel}'.center(LOG_VALUE_WIDTH, ' '))
            others_response = response[OTHERS_RESPONSE]

            if isinstance(others_channel, (list, tuple)):
                for channel, response in zip(others_channel, others_response):
                    logger(channel, response['type'], color='cyan')
                    if channel.startswith(NAMEDGROUP_USER):
                        self.direct_message(channel, response)
                    else:
                        self.group_message(channel, response)

            elif others_channel.startswith(NAMEDGROUP_USER):
                self.direct_message(others_channel, others_response)

            else:
                self.group_message(others_channel, others_response)

    def direct_message(self, group_name: str, msg: dict):
        async_to_sync(self.channel_layer.group_send)(
            group_name,
            {
                'type':    'send_direct_message',
                'mobile':  self.user.mobile,
                'message': msg,
            }
        )

    def group_message(self, group_name: str, msg: dict):
        async_to_sync(self.channel_layer.group_send)(
            group_name,
            {
                'type':    'send_group_message',
                'mobile':  self.user.mobile,
                'message': msg,
            }
        )

    def send_direct_message(self, event: dict):
        try:
            self.send(text_data=json.dumps(event['message']))
        except Exception as e:
            logger('ERROR:', e, color='red')

    def send_group_message(self, event: dict):
        """
        must include 'mobile': self.user.mobile in event when
        sending event to this method
        """
        if self.user.mobile == event.get('mobile'):
            return

        try:
            self.send(text_data=json.dumps(event['message']))
        except Exception as e:
            logger('ERROR:', e, color='red')

