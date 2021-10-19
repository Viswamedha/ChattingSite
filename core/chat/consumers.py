import json

from channels.generic.websocket import AsyncWebsocketConsumer # The class we're using
from asgiref.sync import sync_to_async # Implement later
from .models import Message, Room
from main.models import User

@sync_to_async
def save_message(username, room, message):
    user = User.objects.get(username = username)
    room = Room.objects.get(slug = room)
    Message.objects.create(author = user, room = room, content = message)

class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # print(dir(self.channel_layer))
        # print(self.channel_layer.capacity)
        # Join room group
        await self.channel_layer.group_add(
        self.room_group_name,
        self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
        self.room_group_name,
        self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room']
        await save_message(username, room, message)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
            'type': 'chat.message',
            'message': message,
            'username': username
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))






class NewConsumer(AsyncWebsocketConsumer):

    # async def websocket_connect(self, event):
    #     print(event)
    #     await self.accept()

    # async def websocket_receive(self, event):
    #     print(event["text"])
    #     await self.send({
    #         "type": "websocket.send",
    #         "text": event["text"],
    #     })
    

    async def connect(self):
        
        await self.accept()
        
    
    # async def receive(self, text_data=None, bytes_data=None):
        
    #     await self.send({
    #         "type": "websocket.send",
    #         "text": "text",
    #     })

    async def receive(self, text_data):
        data = json.loads(text_data)
        # print(self.scope)
        print(self.scope['user'])
        print(data)

        if 'Connection' in data:
            print(data['Connection'])
            if data['Connection'] == 1:
                return await self.disconnect(408)
        await self.send(
            text_data=json.dumps({
            'Text': data.get('Text'),
            'User': self.scope['user'].username
        })
        )




class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):   

        await self.accept()

    



'''
class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': message,
                'username': username,
            }
        )

    async def chatroom_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))
'''