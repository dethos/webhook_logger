from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import json


class WebhookConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """While the connection is open, it is associated with a callback id"""
        self.callback = self.scope["url_route"]["kwargs"]["uuid"]
        await self.channel_layer.group_add(self.callback, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.callback, self.channel_name)

    async def receive(self, text_data):
        # Discard all received data
        pass

    async def new_request(self, event):
        """Sends all the newly received data on the callback"""
        await self.send(text_data=json.dumps(event["data"]))
