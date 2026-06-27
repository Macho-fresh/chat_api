from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from accounts.models import *
from chat_app.models import *
from rest_framework import status
from rest_framework.response import Response
import json

class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['group_name']
        self.room_group_name = f"chat_{self.room_name.replace(' ', '_')}"
        try:
            self.room = Group.objects.get(group=self.room_name)
        except Group.DoesNotExist:
            print("GROUP NOT FOUND")
            self.close()
            return

        user = self.scope["user"]

        if not user.is_authenticated:
            print("Login to join a group chat")
            # self.close()
            return
        
        self.chat_user = ChatUser.objects.get(user=user)
        self.chat_user.is_online = True
        self.chat_user.save()

        if user in self.room.members.all():

            self.accept()
            print("CONNECTED")

            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name, self.channel_name
            )
        
        else:    
            print('You are not a member of this group')

    def disconnect(self, code):
        
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name

        )  
        self.chat_user.is_online = False
        self.chat_user.save()

    def receive(self, text_data = None, bytes_data = None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.user = self.scope["user"]


        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f'{self.user.username}: {message}',
            }
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))

class PrivateConsumer(WebsocketConsumer):

    def connect(self):
        # self.user_name = self.scope['url_route']['kwargs']['user']

        self.user = self.scope["user"]
        
        if not self.user.is_authenticated:
            print("Login to chat")
            # self.close()
            return
        
        self.chat_user = ChatUser.objects.get(user=self.user)
        self.chat_user.is_online = True
        self.chat_user.save()
        
        self.user_inbox = self.user.username

        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            f'inbox_{self.user_inbox}', self.channel_name
        )

    def disconnect(self, close_code):

        if self.user.is_authenticated:
            async_to_sync(self.channel_layer.group_discard)(
                f'inbox_{self.user_inbox}',
                self.channel_name,
            )
            self.chat_user.is_online = False
            self.chat_user.save()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        target = text_data_json['target']

        
        if not self.user.is_authenticated:
            print("Login to chat")
            # self.close()
            return
        async_to_sync(self.channel_layer.group_send)(
            f"inbox_{target}", {
                'type': 'private_message',
                'user': self.user.username,
                'message': message,
            }
        )

        self.send(json.dumps({
            'type': 'private_message_delivered',
            'user': f'sent to {target}',
            'message': message,
        }))

        return

    def private_message(self, event):
        self.send(text_data=json.dumps(event))

    def private_message_delivered(self, event):
        self.send(text_data=json.dumps(event))    
