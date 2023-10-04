from django import forms
from django.forms import ModelForm
from reservation.models import   Reservation

#create a venue form
 
class ReservationForm(ModelForm):
	class Meta:
		model = Reservation
		fields = ('name','venue','user','email_address','phone',
			'num_attendees','start_datetime','end_datetime','reason')
		labels = {
			'name':"",'venue':"",'user':"",'email_address':"",'phone':"",'num_attendees':"",'start_datetime':"",
			'end_datetime':"",'reason':""
		}

		widgets = {
			'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Event Name'}),
            'venue': forms.HiddenInput(),  # Use HiddenInput widget for venue
            'user': forms.HiddenInput(),
            'reason':forms.Textarea(attrs={'class':'form-control','placeholder':'purpose of use this facility'}),
			'email_address':forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}),
			'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'phone'}),
			'num_attendees':forms.TextInput(attrs={'class':'form-control','placeholder':'Number of Attendees'}),
			'start_datetime':forms.DateInput(attrs={'class':'form-control','type': 'date', 'placeholder':'mm/dd/yyyy'}),
			'end_datetime':forms.DateInput(attrs={'class':' form-control','type': 'date', 'placeholder':'mm/dd/yyyy'}),	
		}

 