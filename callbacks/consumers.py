from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json


class WebhookConsumer(WebsocketConsumer):
    def connect(self):
        """While the connection of open it is associated with a callback"""
        self.callback = self.scope['url_route']['kwargs']['uuid']
        async_to_sync(self.channel_layer.group_add)(
            self.callback, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.callback, self.channel_name
        )

    def receive(self, text_data):
        # Discard all received data
        pass

    def new_request(self, event):
        """Sends all the newly received data on the callback"""
        self.send(text_data=json.dumps(event["data"]))
