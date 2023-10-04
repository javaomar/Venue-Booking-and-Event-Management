import json 
from django.db.models.signals import post_save 
from .models import ReservationNotify

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.dispatch import receiver

print('YOU ARE IN SIGNAL.PY ')

@receiver(post_save, sender=ReservationNotify)
def send_reservnotification(sender,instance,created,**kwargs):
    if created:
        channel_layer = get_channel_layer()
        reserv_notify = ReservationNotify.objects.filter(approved=False,
            venue__owner=instance.venue.owner).count()
        user = str(instance.venue.owner.id)
        print("New Reservation is created")
        data = {
            'count': reserv_notify
        }

        async_to_sync(channel_layer.group_send)(
            user, {
                'type':'send_reservnotify',
                'value':json.dumps(data)
            }
        )



#send notification when the reservation is approved
@receiver(post_save, sender=ReservationNotify)
def send_onlinestatus(sender, instance, created, **kwargs):
    if not created: 
        channel_layer = get_channel_layer()
        notify_approval = ReservationNotify.objects.filter(approved=True, user=instance.user).count()
        user = str(instance.user.id)
        approval_status = instance.approved
        print(f"The approval is {approval_status}")
        data = {
            'count':notify_approval
        }

        async_to_sync(channel_layer.group_send)(
            user,{
                'type':'send_reservnotify',
                'value':json.dumps(data)
            }
        )

