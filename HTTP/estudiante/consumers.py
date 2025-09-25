import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class EstudianteConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'estudiantes'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        pass

    async def estudiantes_update(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data, ensure_ascii=False))