from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import get_user_model, login, logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
 
from django.urls import reverse_lazy, reverse
from django.views import generic
  
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from .forms import (UserForm, LoginForm, 
	 UpdatePasswordForm, PasswordResetForm)
from django.contrib.auth.forms import PasswordResetForm

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
 
#local files:
 
from .decorators import user_not_authenticated
from .tokens import account_activation_token
from reservation.models import  Reservation
 

class PasswordsChangeView(PasswordChangeView):
	form_class = PasswordChangeForm
	success_url = reverse_lazy('login') 

@user_not_authenticated # check if the user is authenticated
def userlogin(request):

	if request.method == 'POST':
		form = LoginForm(request=request, data=request.POST)
 
		if form.is_valid():
			print('the form is valid')
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			 
			user = authenticate(username=username, password=password)

			if user is not None:
				print('user does exist')
				if user.is_active:
					login(request, user)
					reservations = Reservation.objects.filter(venue__owner=user, approval_status=False )
					reserver = Reservation.objects.filter(user=user, approval_status=True)

					if reservations.exists():
						print('it does')
						count = reservations.filter(approval_status=False).count()
						 
						messages.success(request,f"you have {count} new reservation")
					elif reserver.exists():
 						count = reserver.filter(approval_status=True).count()
 						messages.success(request,f"you reservetion was approved, make an events")
					else:
						messages.success(request,f"welcome back")
					return redirect('events:list-events')
				else:
					print('user not active')
					messages.info(request,f"user not active {user.email} check email for an authentication link.")
					return redirect('accounts:login')
		else:
			print('Invalid username or password.')
			messages.error(request, "Invalid username or password.")
			return redirect('accounts:login')
	else:
		form = LoginForm()
	return render(request, 'registration/login.html', {'form': form})


@login_required
def userlogout(request):
	user = request.user
	logout(request)
	print('logout')
	messages.info(request,f"You logout out @{user.username}")
	return redirect('accounts:login')

'''
below this is the registeration and activation account of a user
'''

def activate(request,uidb64, token):

	User = get_user_model()
	try:
		user_id = force_str(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=user_id)
	except User.DoesNotExist:
		user = None
		print('user doesnt exist') 

	if user is not None and account_activation_token.check_token(user,token):
		user.is_active = True
		user.save()
		print('1000 valid')
		messages.success(request,'your email has been confirm please sign in')
		print('user does exist')
		return redirect('accounts:login')
	else:
		print('2000 invalid')
		messages.error(request,'Activation link is invalid')
 
	return redirect('events:list-events')

def activateEmail(request,user,to_email):
	mail_subject = "Activate your user account"

	message = render_to_string("activation_template.html", {
		'user':user.username, 
		'domain':get_current_site(request).domain, 
		'uid':urlsafe_base64_encode(force_bytes(user.pk)),
		'token':account_activation_token.make_token(user),
		'protocol':'https' if request.is_secure() else 'http',
		})
 
	email = EmailMessage(mail_subject,message,to=[to_email])
	if email.send():
 
		messages.success(request,
			f"Dear <b>{user}</b>, please check your email <b>{to_email}</b> indox \
			and click on the activation link to confirm your account,\
			make sure to check the spam folder two incase..")
 
	else:
 
		message.error(request, f"problem sending email to {to_email}, check if you type it correctly")



@user_not_authenticated # does make sure if the user is authentican if so it won't allow them to register
def register(request):

	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active=False
			user.save()

			# Check if 'email' is a key in form.cleaned_data dictionary
			if 'email' in form.cleaned_data:
				email = form.cleaned_data['email']
				activateEmail(request, user, to_email=email)
				return redirect('accounts:login')
			else:
				messages.error(request, "Email is missing in form data.")

		else:
			for error in list(form.errors.values()):
				print(error)
				messages.error(request,error)

	else:
		form = UserForm()

	return render(request,'accounts/signup.html',{'form':form})



@user_not_authenticated
def passwordreset(request):
	if request.method == 'POST':
		form = PasswordResetForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			# user_query = Q(email=email) | Q(username=username)
			user = get_user_model().objects.filter(Q(email=email)).first()

			if user:
				subject = 'Password Reset request' 
				message = render_to_string("template_reset_password.html", {
					'user':user, 
					'domain':get_current_site(request).domain, 
					'uid':urlsafe_base64_encode(force_bytes(user.pk)),
					'token':account_activation_token.make_token(user),
					'protocol':'https' if request.is_secure() else 'http',
				})

				email = EmailMessage(subject,message,to=[email])
				if email.send():
					messages.success(request,
						f"Dear <b>{user}</b>, please check your email <b>{email}</b> indox \
							and click on the activation link to confirm your account,\
							make sure to check the spam folder two incase..")
					return render(request,'accounts/password_reset_done.html')
				else:
					messages.error(request, f'Problem sending email to this email {user_email}')
			else: 
				messages.error(f'There is no account related to this email: {email}')
				return redirect('accounts:password-reset')
		else:
			for error in list(form.errors.values()):
				print(error)
				messages.error(request,error)
	else:
		form = PasswordResetForm()
	return render(request,'accounts/password_reset_form.html',{'form':form})



def passwordnew(request,uidb64,token):
	User = get_user_model()
	try:
		user_id = force_str(urlsafe_base64_decode(uidb64))
		print(user_id)
		user = User.objects.get(pk=user_id)
	except:
		user = None 
	if user is not None and account_activation_token.check_token(user,token):
		if request.method == 'POST':
			form = UpdatePasswordForm(user,request.POST)
			if form.is_valid():
				form.save()
				messages.success(request,
					'Your password has successfully been reset please login')
				return redirect('accounts:login')
			else:
				for error in list(form.errors.value()):
					messages.error(request,error)
		else:
			form = UpdatePasswordForm(user)
			return render(request,
				'accounts/password_reset_confirm.html', {'form':form})

	else:
		messages.error(request, 'Link has expired')
		return redirect('accounts:login')






