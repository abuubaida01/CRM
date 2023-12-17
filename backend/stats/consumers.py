from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from .models import *


class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["dashboard_slug"]
        self.room_group_name = "chat_%s" % self.room_name

        print("\nCurrent Channel Name", self.channel_layer)
        print("Group Name: ", self.room_name)

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        sender = text_data_json["sender"]

        print("\nReceiver got Message: \t", message)
        print("\n sender is: \t", sender)

        await self.save_data_item(sender, message, slug=self.room_name)
        
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message, "sender": sender,}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        sender = event["sender"]
        await self.send(text_data=json.dumps({"message": message, 'sender':sender}))
    
    @database_sync_to_async
    def create_data_item(self, sender, message, slug):
        obj = Statistic.objects.get(slug=slug)
        return DataItems.objects.create(statistic=obj, value=message, owner=sender) 

    async def save_data_item(self, sender, message, slug):
        await self.create_data_item(sender, message, slug)