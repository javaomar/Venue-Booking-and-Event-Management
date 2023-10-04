import json
from channels.generic.websocket import AsyncWebsocketConsumer
from reservation.models import ReservationNotify
from channels.db import database_sync_to_async 
from django.contrib.auth import get_user_model
User = get_user_model()


class ReservNotification(AsyncWebsocketConsumer):

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

    async def send_reservnotify(self, event):
        data = json.loads(event.get('value'))
        count = data['count']

        await self.send(text_data=json.dumps({
            'count':count
        }))    
        
        

