from django.shortcuts import render, redirect, get_object_or_404
import calendar
from django.contrib.auth import get_user_model
User = get_user_model()

from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Payment, MyClubUser, Ticket
from reservation.models import Reservation
from reservation.forms import ReservationForm
from venue.models import Venue  
from venue.forms import VenueForm 

from .forms import EventForm, PaymentForm,BuyTicketForm,MyClubUserForm
from django.utils.dateformat import format as date_format
from django.http import HttpResponse 
from django.contrib import messages
import csv
import random
from django.core.paginator import Paginator

#pdf imports 
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Spacer,  Table, TableStyle, Image,Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_RIGHT
from reportlab.graphics.barcode import code128
import qrcode
from io import BytesIO
 
from reportlab.platypus import Image as RLImage
###
from django.db.models import Q
#generate transaction ID
import uuid  # For generating unique transaction IDs
from django.db import IntegrityError
'''
Note 
     path Converters
    int: numbers ex year, date
    str: strings
    path: whole urls/   Ex something/something/something
    slug: hyphen-and_underscores_stuff
    UUID: universally unique identifier

'''

 
 

def myclub(request,event_id):
	event = get_object_or_404(Event, id=event_id)
	if request.method == 'POST':
		form = MyClubUserForm(request.POST)
		if form.is_valid():
			myclub = form.save(commit=False)
			myclub.event = event 
			myclub.save() 

			ticket = Ticket(purchaser=myclub)
			ticket.save()
			
			return redirect( 'events:buyticket', ticket_id=ticket.id)
	else:
		initial_data={
			'event':event
		}
		form = MyClubUserForm(initial=initial_data)
	return render(request, 'events/myclub_form.html',{'form':form})

def buyticket(request,ticket_id):
	ticket = get_object_or_404(Ticket,id=ticket_id)
	if request.method == 'POST':
		form = BuyTicketForm(request.POST)
		if form.is_valid():
			buyticket = form.save()
			ticket = buyticket.ticket
			submitted = True

			return render(request,'events/buyticket_form.html',
				{'ticket':ticket, 'submitted':submitted})
	else:
		initial_data = {
			'ticket':ticket
		}
		form = BuyTicketForm(initial=initial_data)
	return render(request,'events/buyticket_form.html',{'form':form})
 
def payment(request,res_id):
	submitted = False
	
	reservation = get_object_or_404(Reservation,id=res_id)
	venue = get_object_or_404(Venue,id=reservation.venue.id)

	if request.method == 'POST':
		form = PaymentForm(request.POST)
		if form.is_valid():
			try:
				form.save()
			except IntegrityError as E:
 
				print(f"Payment Data: {form.data}")
				print(f"IntergrityError: {E}")
				submitted=False 
			else:
				submitted=True
				return render(request,'events/payment.html', {'submitted':submitted})
	else:
		#generate transaction id for each payment method
		def generate_unique_transaction_id():
			while True:
				transaction_id = str(uuid.uuid4())
				try:
					# Attempt to retrieve a Payment record with the generated transaction ID
					payment = Payment.objects.get(transaction_id=transaction_id)
				except Payment.DoesNotExist:
					# Transaction ID does not exist, it's unique, return it
					return transaction_id

		transaction_id = generate_unique_transaction_id()
		initial_data = {
			'venue':venue,'user':request.user.id,'payment_amount':venue.price,
			'payment_date':datetime.now(),'reservation':reservation,
			'transaction_id':transaction_id
		}
		print(initial_data)
		form = PaymentForm(initial=initial_data)
		print(f"Payment_data1: {form.data}")
		# print(f"reservation: {reservation}\n venue: {venue}")
	return render(request, 'events/payment.html',{'form':form,'submitted':submitted})


 
def download_ticket(request, ticket_id):

    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Create a PDF document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{ticket.id}.pdf"'

    # Create the PDF content
    doc = SimpleDocTemplate(response, pagesize=letter)
    story = []

    # Define paragraph styles
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    ticket_number_style = ParagraphStyle(name='TicketNumberStyle', fontSize=14, textColor=colors.black)
    venue_style = ParagraphStyle(name='VenueStyle', fontSize=12)
    Door = [1,2,3,4,5,6]
    letterS = ['A','B','C','D','E','F','I','J','K']
    section = ['One','Two','Three','Four',"Five","Six"]

    random_let = random.choice(letterS)
    random_num = random.randint(1,1000)
    random_combination = f"{random_let}{random_num}"
    # Create a table to structure the ticket content
    data = [
        ["Ticket","","", f"{ticket.purchaser.event.name}"], 
        ["", "","", "Venue", f"{ticket.purchaser.event.venue.name}"],
        ["", "","", "Date", f"{ticket.purchaser.event.event_date}"],
        ["", "","", "Price", f"{ticket.purchaser.event.ticket_price}"],
        ["", "","", "Section",random.choice(section) ,"Door:",random.randint(1,10), "Seat #",random_combination]
    ]

    # Set explicit row heights for each row
    row_heights = [0.4 * inch] * len(data)  # Adjust row heights as needed

    # Create the table for ticket details
    table_style = [
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),  # Set font size for the entire table
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),  # Adjust cell padding
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),  # Align text to the top within cells
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),  # Make the first column bold
    ]

    table = Table(data, colWidths=None, rowHeights=row_heights)
    table.setStyle(TableStyle(table_style))

    # Create a table for QR code and adjust vertical alignment
    qr_code_data = f"https://localhost.com/ticket/{ticket.id}"  # Replace with your actual ticket URL or data

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_code_data)
    qr.make(fit=True)

    qr_code_byte_io = BytesIO()
    qr.make_image(fill_color="black", back_color="white").save(qr_code_byte_io, format="PNG")

    qr_code_image = Image(qr_code_byte_io, width=1.5 * inch, height=2.5 * inch)
    qr_code_image.drawHeight = 1.25 * inch  # Adjust the height as needed
    qr_code_image.drawWidth = 1.25 * inch  # Adjust the width as needed

    qr_code_table = Table([[qr_code_image]], colWidths=0.5 * inch, rowHeights=3 * inch)
    qr_code_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    # Create a vertical barcode with adjusted width
    barcode_value = ticket.purchaser.event.name  # Replace with the value you want to encode in the barcode
    barcode = code128.Code128(barcode_value, barWidth=0.3, barHeight=1.25 * inch)
    barcode_table = Table([[barcode]], colWidths=3, rowHeights=[1.5 * inch])
    barcode_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
	# Rotate the barcode horizontally
    barcode_table.rotate = -90
    # Add the tables to the story
    story.append(Table([[table, qr_code_table]]))  # Place the ticket details, QR code, and barcode side by side

    # Build the PDF document
    doc.build(story)
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


def delete_event(request,event_id):
	event = get_object_or_404(Event, id=event_id)
	event.delete()
	return redirect('events:list-events')

 
def update_event(request,event_id):

	event = get_object_or_404(Event,id=event_id)

	if request.method == "POST":
		form = EventForm(request.POST, instance=event)
		if form.is_valid():
			form.save()
			return render(request,'events/event_detail.html', {'event':event})
	else:
		form = EventForm(instance=event)
		event_date_formatted = event.event_date.strftime('%Y-%m-%dT%H:%M')
		form.fields['event_date'].widget.attrs['value'] = event_date_formatted
		submitted = False
	return render(request,'events/add_event.html', 
		{'form':form, 'submitted':submitted, 'event':event,'update':True})

def event_detail(request,event_id):
	event = get_object_or_404(Event, id=event_id)
	return render(request, 'events/event_detail.html', {'event':event})

def add_event(request,res_id):

	reservation = get_object_or_404(Reservation, id=res_id)

	submitted = False
	if request.method == 'POST':
		form = EventForm(request.POST)
		if form.is_valid():
			if form.cleaned_data['total_tickets'] > reservation.venue.capacity:
				# Add an error message
				print('message')
				messages.error(request, "Total tickets cannot exceed venue capacity of {}.".format(venue.capacity))	
			else:
				event = form.save()
				messages.success(request, '{event.name} has been successfully created!! Please Make a payment')
				
				return redirect('events:payment', res_id =event.reservation.id )
				# return redirect('events:list-events')
	else:
		initial_data = {
			'manager':request.user,'venue':reservation.venue,'total_tickets':reservation.venue.capacity,'reservation':reservation,
			'available_tickets':reservation.venue.capacity
		}

		form = EventForm(initial=initial_data)
		submitted = False
	return render(request,'events/add_event.html',{'form':form,'submitted':submitted})

 
def all_events(request):
	# user = User.objects.exclude(useranme=request.user.username)
	events = Event.objects.all().order_by('name')

	return render(request,'events/event_list.html',{"events":events,})



# Welcoming Page
def home(request): 
	now = datetime.now()
	current_year = now.year
	# #current time
	time = now.strftime('%I:%M:%S %p')
	return render(request, 'index.html', {'year':current_year})
 
 