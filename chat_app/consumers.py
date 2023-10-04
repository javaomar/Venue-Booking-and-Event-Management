import json 
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from accounts.models import CustomUser
from chat_app.models import ChatModel, MessageNotification
 
from django.contrib.auth import get_user_model
User = get_user_model()


#chatconsumer connections websocket
class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        my_id = self.scope['user'].id
        user_other_id = self.scope['url_route']['kwargs']['id']

        if int(my_id) < int(user_other_id):
            self.room_name = f"{user_other_id}-{my_id}"
        else:
            self.room_name = f'{my_id}-{user_other_id}'
        
        self.room_group_name = 'chat_%s'%self.room_name 

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        # await self.send(text_data=self.room_group_name)

    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self,text_data=None, byte_data=None):
        data = json.loads(text_data)

        message = data['message']
        username = data['username']
        receiver = data['receiver']

        await self.save_message(username, receiver, message, self.room_group_name)

        await self.channel_layer.group_send(
            self.room_group_name,{
                
                'type':'chat_message',
                'message':message,
                'username':username,
                'receiver':receiver,
            }
        )
    async def chat_message(self,event):
        message = event['message']
        username = event['username']
        receiver = event['receiver']

        await self.send(text_data=json.dumps({
            'message':message,
            'username':username,
            'receiver':receiver,
        }))

    @database_sync_to_async
    def save_message(self,username,receiver,message,room_name):
        sender_user = CustomUser.objects.get(username=username)
        receiver_user = CustomUser.objects.get(username=receiver)
        chat  = ChatModel.objects.create(
            sender=sender_user,
            receiver=receiver_user,
            message=message,
            room_name=room_name,
        )
        other_user_id = self.scope['url_route']['kwargs']['id']
        # print(f'other_user_id:{other_user_id}')
        get_user = User.objects.get(id=other_user_id)
        if receiver == get_user.username:
            print(f"chat:{chat.room_name}")
            MessageNotification.objects.create(chat=chat ,user=get_user)
            # print(f'notification receiver:{receiver_user.id}')
        
 

class ChatNotification(AsyncWebsocketConsumer):
    async def connect(self):
        user_id = self.scope['user'].id
        self.room_group_name = f"{user_id}"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name 
        )

        await self.accept()

    async def disconnect(self, code):
        self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name 
        )
    
    async def send_notification(self, event):
        data = json.loads(event.get('value'))
        count = data['count']
        print(f"notif receiver: {count}")
        await self.send(text_data=json.dumps({
            'count':count
        }))