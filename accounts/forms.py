from django import forms
from django.contrib.auth import get_user_model #it return the current user
from django.contrib.auth.forms import (UserCreationForm, AuthenticationForm,
	SetPasswordForm, PasswordResetForm)
# from captcha.fields import ReCaptchaField
# from captcha.widgets import ReCaptchaV2Checkbox


class UserForm(UserCreationForm):
	email = forms.EmailField(
		help_text='Valid Email required',
		# label={'email':""},
		widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
		required=True)
	password1 = forms.CharField(
        help_text="Password must match",
        widget=forms.PasswordInput(attrs={'class': 'form-control','autocomplete': 'new-password', 'placeholder': 'Password'}),
        required=True,
 
    )
	password2 = forms.CharField(
		help_text="Password must match",
		widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
		required=True
    )
	class Meta:
		model = get_user_model()
		fields = ('first_name','last_name','username',
			'email','status','password1','password2',)




		labels = {
			'first_name':"",'last_name':"",'username':"",
			'email':"",'status':"",'password1':"",'password2':"",
		}
		
		widgets = {
	        'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
	        'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
	        'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
	        'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
	        'status':forms.Select(attrs={'class':'form-select','placeholder':'select'}),
	        'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
	        'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
	    }

	# captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
	def save(self, commit=True):
		user = super(UserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit: 
			user.save()
		return user



class LoginForm(AuthenticationForm):
	def __init__(self,*args,**kwargs):
		super(LoginForm, self).__init__(*args,**kwargs)

	username = forms.CharField(widget=forms.TextInput(
		attrs={'class':'form-control','placeholder':'Username or Email'}
		),label="")
	password = forms.CharField(widget=forms.PasswordInput(
		attrs={'class':'form-control','placeholder':'Password'}
		),label="")

class UpdatePasswordForm(SetPasswordForm):
	class Meta:
		model = get_user_model()
		fields = ['new_password1','new_password2']

 
'''
this form is the form used to collect the email to reset the password
'''
class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(Password_ResetForm, self).__init__(*args, **kwargs)







