from django.shortcuts import render
from accounts.models import CustomUser
from .models import ChatModel
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.
''' 
in this app it's main response is to connect the User ispacialy venue onwer and the renters
'''

def chatroom(request, username):
    all_user = CustomUser.objects.exclude(username=request.user.username)
    if username == "None":
        user = User.objects.get(username=all_user[0])
    else: 
        user = User.objects.get(username=username)
    print(f"request_id: {request.user.id} user_id: {user.id}")

    if request.user.id > user.id:
        room_name = f"chat_{request.user.id}-{user.id}"
    else:
        room_name = f"chat_{user.id}-{request.user.id}"

    messages = ChatModel.objects.filter(room_name=room_name)

    return render(request, 'chat_app/room.html',{
        'users':all_user,'user':user, 'messages':messages
    })