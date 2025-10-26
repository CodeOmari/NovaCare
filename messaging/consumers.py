from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.contrib.auth.models import User
from .models import Conversation, Message
from .utils import set_user_online, set_user_offline
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    # Runs when a user connects
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'
        user = self.scope["user"]

        # Mark user as online
        if user.is_authenticated:
            set_user_online(user.id)

        # Join the chat room
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()  # Accept the WebSocket connection

    # Runs when user disconnects
    async def disconnect(self, close_code):
        user = self.scope["user"]
        if user.is_authenticated:
            set_user_offline(user.id)
        # Leave the chat group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        sender_id = self.scope["user"].id

        # Save message in DB
        conversation = await self.get_conversation(self.conversation_id)
        sender = await self.get_user(sender_id)
        msg = await self.save_message(conversation, sender, message)

        # Send message to everyone in the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',  # function name to call below
                'sender': sender.username,
                'message': message,
                'timestamp': str(msg.timestamp)
            }
        )

    # Broadcast message to WebSocket clients
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    async def get_conversation(conversation_id):
        return Conversation.objects.get(id=conversation_id)

    @database_sync_to_async
    async def get_user(user_id):
        return User.objects.get(id=user_id)
    
    @database_sync_to_async
    def save_message(self, conversation, sender, content):
        return Message.objects.create(conversation=conversation, sender=sender, content=content)




# connect() — triggered when a user opens the chat. Adds them to a chat room.
# disconnect() — runs when user leaves; marks them offline.
# receive() — handles messages coming in from frontend → saves to DB → broadcasts to all users in the room.
# chat_message() — sends data back to browser clients in real-time.