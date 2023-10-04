from django.shortcuts import render, redirect, get_object_or_404
import calendar
from django.contrib.auth import get_user_model
User = get_user_model()

 
 
from django.http import HttpResponseRedirect
from .models import  Venue 
from .forms import VenueForm
from events.forms import EventForm, PaymentForm,BuyTicketForm,MyClubUserForm
from reservation.forms import ReservationForm
from reservation.models import Reservation
from django.utils.dateformat import format as date_format
 
from django.contrib import messages
 

#pdf imports
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Spacer,  Table, TableStyle, Image,Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_RIGHT
from reportlab.graphics.barcode import code128
import qrcode
from io import BytesIO
 
###
import io 
 
#generate transaction ID
import uuid  # For generating unique transaction IDs
 
 
 
 
def venue_pdf(request):
	#create bytestream buffer 
	buf = io.BytesIO()
	#create a canvas
	c = canvas.Canvas(buf, pagesize=letter,bottomup=0)
	#create a text object
	textob = c.beginText()
	textob.setTextOrigin(inch,inch)
	textob.setFont('Helvetica',14)

	#add some Lines of text
	lines = []
	# lines = [
	# 	'this is line 1',
	# 	'this is line 2',
	# 	'this is line 3',
	# ]
	venues = Venue.objects.all()
	for venue in venues:
		lines.append(venue.name)
		lines.append(venue.address)
		lines.append(venue.zip_code)
		lines.append(venue.phone)
		lines.append(venue.web)
		lines.append(venue.email_address)
		lines.append(" ")

	for line in lines:
		textob.textLine(line)

	c.drawText(textob)
	c.showPage()
	c.save()
	buf.seek(0)


	return FileResponse(buf,as_attachment=True, filename='veneu.pdf')

# Generate CSV File Venue List
def venue_csv(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=venues.csv'
	
	# Create a csv writer
	writer = csv.writer(response)

	# Designate The Model
	venues = Venue.objects.all()

	# Add column headings to the csv file
	writer.writerow(['Venue Name', 'Address', 'Zip Code', 'Phone', 'Web Address', 'Email'])

	# Loop Thu and output
	for venue in venues:
		writer.writerow([venue.name, venue.address, venue.zip_code, venue.phone, venue.web, venue.email_address])

	return response


def venue_text(request):
	response = HttpResponse(content_type='text/plain')
	response['Content-Disposition'] = 'attachment; filename=venues.txt'
	#Designate the Model
	venues = Venue.objects.all()

	# Create blank list
	lines = []
	# Loop Thu and output
	for venue in venues:
		lines.append(f'Name: {venue.name}\nAddress: {venue.address} Zip: {venue.zip_code}\nPhone: {venue.phone}\nWeb: {venue.web}\nEmail: {venue.email_address}\n\n\n')

	#lines = ["This is line 1\n", 
	#"This is line 2\n",
	#"This is line 3\n\n",
	#"John Elder Is Awesome!\n"]

	# Write To TextFile
	response.writelines(lines)
	return response


 
def delete_venue(request,venue_id):
	venue= get_object_or_404(Venue, id=venue_id)
	name = venue.name
	venue.delete()
	messages.success(request,f"venue {name} has successfully been deleted" )
	return redirect('venues:list-venues')
	 

  

def search_venues(request):
	searched = None
	venues = []
	if request.method=="POST":
		searched = request.POST['searched'] 	

		venues = Venue.objects.filter(name__contains=searched)
 
		return render(request, 'venue/search_venue.html',
			{'searched':searched,'venues':venues})
	else:
		return render(request,'venue/search_venue.html', {})

def show_venue(request,venue_id):
	venue = get_object_or_404(Venue, id=venue_id)
	return render(request,'venue/show_venue.html',{"venue":venue})

def list_venues(request):
	venues = Venue.objects.all()

	#make pagination 
	# p = Paginator(Venue.objects.all(), 4)
	# page = request.GET.get('page')
	# venues = p.get_page(page)
	# nums = "a" * venues.paginator.num_pages
	# return render(request, 'venue/venue.html', 
	# 	{'venue_list': venue_list,
	# 	'venues': venues,
	# 	'nums':nums}
	# 	)
	return render(request, 'venue/venue.html', { 'venues': venues})

def add_venue(request):
	submitted = False
	if request.method == 'POST':
		form = VenueForm(request.POST,request.FILES)
		if form.is_valid():
			print(request.FILES)
			print('picture False')
			venue = form.save()
			print(venue.id)
			# venue = venue
			return redirect('venues:show-venue',venue_id=venue.id)
			# return render(request, 'venue/show_venue.html', {'veune':venue})
			# return HttpResponseRedirect('/venue/add_venue/?submitted=True')
	else:
		initial_data ={'owner':request.user}
		form = VenueForm(initial=initial_data)
		if 'submitted' in request.GET:
			submitted = True
	return render(request, 'venue/add_venue.html', {'form':form, "submitted":submitted})

 
def update_venue(request,venue_id):
	venue = get_object_or_404(Venue, id=venue_id)

	if request.method == 'POST':
		form = VenueForm(request.POST,request.FILES, instance=venue)
		if form.is_valid():
			form.save()
			return render(request,'venue/show_venue.html',{"venue":venue})
	else:
		form = VenueForm(instance=venue)
		submitted = False
	return render(request, 'venue/add_venue.html', {'form':form, "submitted":submitted, 'venue':venue})


 