from django import forms
from django.forms import ModelForm
from .models import Venue


#create a venue form
class VenueForm(ModelForm):
	class Meta:
		model = Venue
		# fields = "__all__" you will use all field or selected field like below
		fields = ('name', 'owner','address', 'zip_code', 'phone', 'web','email_address','price',
			'capacity','picture','descriptions')
		labels = {
			'name':"",
			'owner':"",
			'address':"",
			'zip_code':"",
			'descriptions':"",
			'phone':"",
			'web':"",
			'email_address':"",
			'price':"",
			'capacity':"",'picture':"",
		}

		widgets = {
		'name':forms.TextInput(attrs={'class':'form-control','placeholder':'Venue Name'}),
		'owner':forms.HiddenInput(),
		'address':forms.TextInput(attrs={'class':'form-control','placeholder':'address'}),
		'descriptions':forms.Textarea(attrs={'class':'form-control'}),
		'zip_code':forms.TextInput(attrs={'class':'form-control','placeholder':'zip code'}),
		'phone':forms.TextInput(attrs={'class':'form-control','placeholder':'phone'}),
		'web':forms.TextInput(attrs={'class':'form-control','placeholder':'web'}),
		'email_address':forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}),
		'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
		'capacity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Capacity'}),
		'picture': forms.FileInput(attrs={'class': 'form-control'}),
		}
 