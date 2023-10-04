from django.urls import path

from reservation import consumers 




Re_websocket_urlpatterns = [
	path('ws/reservation/',consumers.ReservNotification().as_asgi()),
] 