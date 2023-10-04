from django.contrib import admin	
from .models import Event,Venue, MyClubUser, Payment

admin.site.register(Venue)
admin.site.register(Event)
admin.site.register(MyClubUser)
admin.site.register(Payment)
 
