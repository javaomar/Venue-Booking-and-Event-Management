from django.contrib import admin
from .models import ChatModel, MessageNotification

# Register your models here.
admin.site.register(ChatModel)
admin.site.register( MessageNotification)

 