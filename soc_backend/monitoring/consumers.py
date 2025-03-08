import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Alert

class AlertConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("alerts", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("alerts", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')

        if message:
            alert = await sync_to_async(Alert.objects.create)(
                user_id=1,  # Change this to the correct user ID
                message=message
            )

            await self.channel_layer.group_send(
                "alerts",
                {
                    "type": "send_alert",
                    "message": message
                }
            )

    async def send_alert(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
