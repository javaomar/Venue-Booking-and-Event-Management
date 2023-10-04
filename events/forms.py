from django import forms
from django.forms import ModelForm
from .models import  Event, Payment,BuyTicket, MyClubUser


 
class PaymentForm(ModelForm):
	class Meta:
		model = Payment 
		fields = ('user','venue','transaction_id','card_type','card_name',
			'card_number','card_date','card_security','payment_amount',
			 'reservation')
		labels = { 'user':"",'venue':"",'transaction_id':"",'card_type':"",'card_name':"",
			'card_number':"",'card_date':"",'card_security':"",'payment_amount':"",
			  'payment_status':"",'reservation':"",
		}

		widgets = {
			'user':forms.HiddenInput(),
			'venue':forms.HiddenInput(),

			'card_type':forms.Select(attrs={'class':'form-select','placeholder':"MASTER or VISE"}),
			'card_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Name on Card'}),
			'card_number':forms.TextInput(attrs={'class':'form-control','placeholder':'Card Number'}),
			'card_date':forms.TextInput(attrs={'class':'form-control','placeholder':'Experetion Date'}),
			'card_security':forms.TextInput(attrs={'class':'form-control','placeholder':'Security Code'}),
			'payment_amount':forms.TextInput(attrs={'class':'form-control','placeholder':"Amount"}),

			'transaction_id':forms.HiddenInput(),
			 
			'payment_status':forms.HiddenInput(),
			'reservation':forms.HiddenInput(),

		}
 
 
class EventForm(ModelForm):
	class Meta: 
		model = Event
		fields = ('name','speaker','event_date','venue','manager','total_tickets',
			'description','reservation','ticket_price')
		labels= {'name':"",'speaker':"",'event_date':"",'venue':"",'manager':"",'total_tickets':"",
			'description':"",'reservation':"","ticket_price":"", 
		}

		widgets={
			'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Event Name'}),
			'speaker':forms.TextInput(attrs={'class':'form-control','placeholder':'Speaker'}),
			'event_date':forms.DateInput(attrs={'class':' form-control','type': 'datetime-local','placeholder':'Date' }),
			'venue':forms.HiddenInput(),
			'manager':forms.HiddenInput(),
			'reservation':forms.HiddenInput(),
			'total_tickets':forms.TextInput(attrs={'class':'form-control','placeholder':'Total Guest'}),
			'description':forms.Textarea(attrs={'class':'form-control','placeholder':'description'}),
			'ticket_price':forms.TextInput(attrs={'class':'form-control','placeholder':'$price'})
	 	 }


	def __init__(self, *args, **kwargs):
		super(EventForm, self).__init__(*args, **kwargs)
		self.fields['venue'].widget.choices = [('', 'Venue')] + list(self.fields['venue'].widget.choices)[1:]
		self.fields['manager'].empty_label = 'Manager'



class BuyTicketForm(ModelForm):
	class Meta:
		model = BuyTicket
		fields = ('first_name','last_name','email','ticket','card_type',
			'card_name','card_number','card_date','card_security','card_security',
			'payment_amount',)
		labels = { 'first_name':"",'last_name':"",'email':"",'ticket':"",'card_type':"",'card_name':"",
			'card_number':"",'card_date':"",'card_security':"",'payment_amount':"",
		}
		widgets = {
			'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
			'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
			'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}),
			'ticket':forms.HiddenInput(),
			'card_type':forms.Select(attrs={'class':'form-select','placeholder':"MASTER or VISE"}),
			'card_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Name on Card'}),
			'card_number':forms.TextInput(attrs={'class':'form-control','placeholder':'Card Number'}),
			'card_date':forms.TextInput(attrs={'class':'form-control','placeholder':'Experetion Date'}),
			'card_security':forms.TextInput(attrs={'class':'form-control','placeholder':'Security Code'}),
			'payment_amount':forms.TextInput(attrs={'class':'form-control','placeholder':"Amount"}),

		}


class MyClubUserForm(ModelForm):
	class Meta:
		model = MyClubUser
		fields = ('first_name','last_name','email','event')
		labels = { 'first_name':"",'last_name':"",'email':"",'event':"",
		}
		widgets = {
			'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
			'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
			'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}),
			'event':forms.HiddenInput()
		}

