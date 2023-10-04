from django.urls import path

from chat_app import consumers 




websocket_urlpatterns = [
	path('ws/<int:id>/',consumers.ChatConsumer.as_asgi()),
	path('ws/notify/',consumers.ChatNotification().as_asgi()),
	path('ws/notifytwo/',consumers.ChatNotification().as_asgi()),
] 