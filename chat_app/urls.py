from django.urls import path, include 
from chat_app import views

app_name = 'chat_app'

urlpatterns = [
    path('room/<str:username>', views.chatroom, name='chat'),
]