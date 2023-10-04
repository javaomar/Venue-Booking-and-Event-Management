from django.shortcuts import render, redirect, get_object_or_404
import calendar
from django.contrib.auth import get_user_model
User = get_user_model()

  
from datetime import datetime
 
from .models import  Reservation, ReservationNotify
from venue.models import Venue  
from events.forms import EventForm, PaymentForm,BuyTicketForm,MyClubUserForm
from events.models import Event, Payment, MyClubUser, Ticket
from reservation.forms import ReservationForm
from django.utils.dateformat import format as date_format
 
from django.contrib import messages
import csv
from django.core.paginator import Paginator

#pdf imports
 
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
#generate transaction ID
 
 

'''
These are the codes that handels the reservation part of project

'''
 
 
@login_required
def cancel_reservation(request, res_id ):
	if request.method == 'POST':
		reservation = get_object_or_404(Reservation, id=res_id)
		reservation.approval_status = False
		reservation.save()
		user = request.user 
		reservations = Reservation.objects.filter(venue__owner=user)
		return render(request, 'reservation/reservation_venue.html', {'reservation':reservation})
	else:
		reservation = get_object_or_404(Reservation, id=res_id)
		print(f'Reservation Name: {reservation.name}')
		return render(request, 'reservation/reservation_cancel.html', {'reservation':reservation})
@login_required
def reserv_owner_cancel(request, res_id):
	reservation = Reservation.objects.get(id=res_id)
	venue = reservation.venue 
	reservation.delete()
	#redirect to the notify page 
	user = request.user 
	user_reservations = Reservation.objects.filter(user=user,approval_status=True )
	venue_reservation = Reservation.objects.filter(venue__owner=user, approval_status=False)

	messages.success(request,f"{venue.name} reservation has successfully been canceled .")

	return render(request, 'reservation/reservation.html', 
		{'user_reservations': user_reservations,'venue_reservation':venue_reservation})

 
@login_required
def disapproved_reservation(request,res_id,):
	reserv = get_object_or_404(Reservation, id=res_id)
	reserv.delete()
	user = request.user 
	reservation = Reservation.objects.filter(venue__owner=user)
	return render(request, 'reservation/reservation_venue.html', {'reservation':reservation})

@login_required
def approved_reservation(request,res_id):
	reservation = get_object_or_404(Reservation, id=res_id)
 	# Update reservation approval and payment status

	reservation.approval_status = True
 
	reservation.save()


	# Bulk update ReservationNotify objects
	check = get_object_or_404(ReservationNotify,reservation=reservation)
	# check = ReservationNotify.objects.get(reservation=reserv, venue__owner=request.user)
	 
	check.approved = True
	check.is_seen = True 
	check.save()
	# ReservationNotify.objects.filter(reservation=reserv, venue__owner=request.user).update(
    #     approved=True,
    #     is_seen=True

    # )
	# print(f"{check.reservation}2:{check.approved}")
	# reservations = Reservation.objects.filter(venue__owner=request.user )
	return render(request, 'reservation/reservation_venue.html', {'reservation':reservation})


@login_required
def reservation_venue(request, res_id):
	#show that perticular reservation that the onwer need to approve or disprove
 
	reservation = get_object_or_404(Reservation, id=res_id)
	res_id = reservation.id
	print(f"reservation_id:{reservation.id}")
	return render(request, 'reservation/reservation_venue.html', {'reservation':reservation, 'res_id':reservation.id})

@login_required
def user_reservation(request):
	user = request.user
	#getting hold of the reservation the user made
	user_reservations = Reservation.objects.filter(user=user,approval_status=True )
	venue_reservation = Reservation.objects.filter(venue__owner=user, approval_status=False)


	return render(request, 'reservation/reservation.html', 
		{'user_reservations': user_reservations,'venue_reservation':venue_reservation})

 
@login_required
def reservation(request,venue_id):
	venue = get_object_or_404(Venue,id=venue_id)

	if request.method == "POST":
		form = ReservationForm(request.POST)
		if form.is_valid():
			print(form.cleaned_data)
			res = form.save()
			# create Notification for the reservation 
			 
			ReservationNotify.objects.create(
				reservation=res,
				user=request.user,
				venue=res.venue,
			)

			messages.success(request, "Your reservation was successful, you will be notify if approved")
			return redirect('venues:list-venues')

	else:
		initial_data = {
			'venue': venue,
			'user': request.user,
		}
		form = ReservationForm(initial=initial_data)
	return render(request, 'reservation/reservation_form.html', {'form':form,'venue':venue})
 
 
 
 