from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from accounts.models import CustomUser
User = get_user_model()
# Create your models here.


class ChatModel(models.Model):
    sender = models.ForeignKey(to=User, on_delete=models.CASCADE,related_name='sent_message', default=None)
    receiver = models.ForeignKey(to=User, on_delete=models.CASCADE,related_name='received_message',default=None)
    message = models.TextField(null=True,blank=True)
    room_name = models.CharField(null=True, blank=True, max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.room_name 
 

class MessageNotification(models.Model):
    chat = models.ForeignKey(ChatModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

