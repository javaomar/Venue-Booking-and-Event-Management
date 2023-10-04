from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from venue.models import Venue 
from reservation.models import Reservation
User = get_user_model()
import random

from django.template.defaultfilters import slugify
import os


from django.utils import timezone
import misaka 

 
class Payment(models.Model):
	CARD_CHOICES = [
		('mastercard', 'MasterCard'),
		('visacard', 'VisaCard'),
	]
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	venue = models.ForeignKey(Venue,on_delete=models.CASCADE, related_name='payment')
	transaction_id = models.CharField(max_length=100, unique=True)
	card_type = models.CharField(max_length=20,choices=CARD_CHOICES)
	card_name = models.CharField(max_length=250)
	card_number = models.CharField(max_length=450)
	card_date = models.CharField(max_length=250,)
	card_security = models.CharField(max_length=100)
	payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
	payment_date = models.DateTimeField(auto_now_add=True)
	payment_status = models.BooleanField(default=False)
	reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='payment',null=True )
	def __str__(self):
		return f"Payment by {self.user.username} - ${self.venue.price}"

	class Meta:
		unique_together = ('venue','user')



class Event(models.Model):
	name = models.CharField('Event Name', max_length=120)
	speaker = models.CharField('Speaker',max_length=250,blank=True,null=True)
	event_date= models.DateTimeField('Event Date')
	venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE, related_name="event")
	reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, null=True, blank=True, related_name="event_reservation")
	manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
	description = models.TextField(default='',blank=True)
	description_html = models.TextField(editable=False,default='',blank=True)
	total_tickets = models.PositiveIntegerField(default=0)
	available_tickets = models.PositiveIntegerField(default=0)
	ticket_price =  models.PositiveIntegerField(default=0)
	payment = models.BooleanField(default=False)

	def __str__(self):
		return self.name


	class Meta:
		ordering = ['-event_date']

	def save(self,*args,**kwargs):
		self.description_html = misaka.html(self.description)
		super().save(*args,**kwargs)
		
class MyClubUser(models.Model):
	first_name = models.CharField('First Name',max_length=30)
	last_name = models.CharField('Last Name',max_length=30)
	event = models.ForeignKey(Event, related_name='myclub',on_delete=models.CASCADE,default='')

	email = models.EmailField('User Email', max_length=40)

	def __str__(self):
		return self.first_name + ' ' + self.last_name
	class Meta: 
		ordering = ['last_name']

class Ticket(models.Model):
	purchaser = models.ForeignKey(MyClubUser, on_delete=models.CASCADE, related_name='myclub')
	ticket_number = models.CharField(max_length=20, unique=True, default='')  # Adjust the max_length as needed

	def save(self, *args, **kwargs):
		if not self.ticket_number:
			myclub_user = self.purchaser 
			# Generate a unique ticket number based on event and purchaser
			event_info = slugify(myclub_user.event)
			purchaser_info = slugify(self.purchaser)
			unique_slug = f"{event_info}-{purchaser_info}"
			base_ticket_number = unique_slug[:10]  # Adjust the length as needed
			counter = 1
			while True:
				ticket_number = f"{base_ticket_number}-{counter}"
				if not Ticket.objects.filter(ticket_number=ticket_number).exists():
					break
				counter += 1
			self.ticket_number = ticket_number	

		super().save(*args, **kwargs)

	class Meta:
		ordering = ['ticket_number']


class BuyTicket(models.Model):
	CARD_CHOICES = [
		('mastercard', 'MasterCard'),
		('visacard', 'VisaCard'),
	]
	first_name = models.CharField('First Name',max_length=250)
	last_name = models.CharField('Last Name',max_length=250)
	email = models.EmailField('User Email', max_length=40)
	ticket = models.ForeignKey(Ticket, on_delete=models.SET_NULL, null=True)
	card_type = models.CharField(max_length=20,choices=CARD_CHOICES)
	card_name = models.CharField(max_length=250)
	card_number = models.CharField(max_length=450)
	card_date = models.CharField(max_length=250,)
	card_security = models.CharField(max_length=100)
	payment_amount = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.first_name + ' ' + self.last_name
	class Meta: 
		ordering = ['last_name']
 