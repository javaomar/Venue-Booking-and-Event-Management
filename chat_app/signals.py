import json 
from django.db.models.signals import post_save 
from .models import MessageNotification

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.dispatch import receiver

print('YOU ARE IN SIGNAL.PY ')

@receiver(post_save, sender=MessageNotification)
def send_notification(sender, instance, created, **kwargs):
    if created: 
        channel_layer = get_channel_layer()
        notify_obj = MessageNotification.objects.filter(is_seen=False, user=instance.user).count() 
        user_id =str(instance.user.id)
        print(f"User:{user_id} notigy:{notify_obj}")
        data = {
            "count":notify_obj
        }
        print(f"Signal Is_created: {notify_obj}")
        async_to_sync(channel_layer.group_send)(
            user_id,{
                'type':'send_notification',
                'value':json.dumps(data)
            }
        )



