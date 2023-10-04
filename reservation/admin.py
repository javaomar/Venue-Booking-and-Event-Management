from django.contrib import admin
from .models import Reservation,ReservationNotify
# Register your models here.

admin.site.register(ReservationNotify)
admin.site.register(Reservation)