import json
from channels.generic.websocket import AsyncWebsocketConsumer
import redis

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        print(f"Connecting to room: {self.room_group_name}")

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print("Connection accepted")

    async def disconnect(self, close_code):
        print(f"Disconnecting from room: {self.room_group_name}")
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print("Disconnected")

    async def receive(self, text_data):
        print(f"Received message: {text_data}")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Save message to Redis
        await self.save_message(self.room_name, message)
        print(f"Message saved to Redis: {message}")

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        print(f"Message sent to group: {self.room_group_name}")

    async def chat_message(self, event):
        message = event['message']
        print(f"Chat message event: {message}")

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
        print("Message sent to WebSocket")

    async def save_message(self, room, message):
        r = redis.Redis()
        r.rpush(room, message)
        print(f"Message {message} saved to Redis room {room}")
