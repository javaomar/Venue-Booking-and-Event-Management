from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
User = get_user_model()
import random

from venue.models import Venue 

from django.template.defaultfilters import slugify
import os
 
from django.utils import timezone
import misaka 

# Create your models here.
 
class Reservation(models.Model):
	name = models.CharField('Manager Name', max_length=120, null=True)
	venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='reservation')
	reason = models.TextField(blank=True,null=True, max_length=1000)
	reason_html = models.TextField(editable=False,default='',blank=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservation')
	email_address = models.EmailField('Email Address', max_length=40, blank=True)
	phone = models.CharField('Contact Phone', max_length=25, blank=True)
	num_attendees = models.IntegerField()
	start_datetime = models.DateTimeField()
	end_datetime = models.DateTimeField()
	approval_status = models.BooleanField(default=False)


	def __str__(self):
		return f"{self.venue.name} - {self.start_datetime} to {self.end_datetime}"


	def save(self,*args,**kwargs):
		self.reason_html = misaka.html(self.reason)
		super().save(*args,**kwargs)
	class Meta:
		unique_together = ('venue','user')
class ReservationNotify(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

