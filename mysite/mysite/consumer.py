from channels.generic.websocket import AsyncWebsocketConsumer
import json

class VideoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        pass   