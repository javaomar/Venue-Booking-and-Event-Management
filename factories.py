import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE','myclub_website.settings')

import django
django.setup()

import factory
from faker import Faker
from django.core.files import File  
from events.models import Event, MyClubUser
from venue.models import Venue 
from django.contrib.auth.models import User
from events.forms import  EventForm  # Import your custom forms
from venue.forms import VenueForm
from accounts.models import CustomUser 
import random

image_folder = 'venue_pictures'
image_extensions = ['.jpg', '.jpeg', '.png', '.gif']  # Add other extensions as needed
image_files = [filename for filename in os.listdir(image_folder) if os.path.splitext(filename)[1].lower() in image_extensions]
fake = Faker()
 
 
 

class VenueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Venue

    # name = fake.company()
    name = factory.Sequence(lambda n: f'Venue {Venue.owner} {n}')
    address = fake.address()
    zip_code = fake.zipcode()
    phone = fake.phone_number()
    web = fake.url()
    descriptions = fake.paragraph(nb_sentences=25)
    email_address = fake.email()
    owner = CustomUser.objects.order_by('?').first()
    price= fake.random_int(min=2500, max=250000)
    capacity=fake.random_int(min=250, max=60000)
  

    # @factory.lazy_attribute
    # def picture(self):
    #     # Get a list of image files in the 'venue_pictures' folder
    #     image_folder = 'venue_pictures'
    #     image_extensions = ['.jpg', '.jpeg', '.png', '.gif']  # Add other extensions as needed
    #     image_files = [filename for filename in os.listdir(image_folder) if os.path.splitext(filename)[1].lower() in image_extensions]

    #     # Check if there are any image files in the folder
    #     if image_files:
    #         # Select a random image file from the list
    #         image_file_path = os.path.join(image_folder, random.choice(image_files))

    #         with open(image_file_path, 'rb') as file:
    #         # Create a Django File object from the image file
    #             django_file = File(file)
    #             # Set the filename for the File object (e.g., 'image.jpg')
    #             django_file.name = os.path.basename(image_file_path)

    #         return django_file
    #     else:
    #         # No image files found, return None or handle as needed
    #         return None

class MyClubUserFactory(factory.Factory):
    class Meta:
        model = MyClubUser

    first_name = fake.first_name()
    last_name = fake.last_name()
    event = Event.objects.order_by('?').first()
    email = fake.email()

class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    venue = factory.SubFactory(VenueFactory)
    name = fake.catch_phrase()
    event_date = fake.date_time_this_year()
    manager = factory.SelfAttribute('venue.owner')  # Set the manager as the owner of the venue
    total_tickets = factory.SelfAttribute('venue.capacity')
    available_tickets = factory.SelfAttribute('venue.capacity')
    ticket_price = fake.random_int(min=2500, max=250000)
    description = fake.paragraph()
 

def fake_date(num_date):
    existing_users = CustomUser.objects.all()
    venue_form = VenueForm()
    event_form = EventForm()

    image_folder = 'venue_pictures'
    image_files = [filename for filename in os.listdir(image_folder)]
    for i in range(num_date):
    #     manager = existing_users.order_by('?').first()
        venue = VenueFactory.create()

    #     # Create an Event instance with fake data using EventFactory
    #     event = EventFactory.create(venue=venue)

    #     # Print the created objects
    #     print('here are the venue and event')
    #     print(venue)
    #     print(venue.picture)
    #     print(event)
    #     print(event.name)

        # Create a Venue instance with fake data using VenueForm
        manager = existing_users.order_by('?').first()


        venue_data = {
            'name': fake.company(),
            'address': fake.address(),
            'zip_code': fake.zipcode(),
            'owner': manager,
            'phone': fake.phone_number(),
            'web': fake.url(),
            'email_address': fake.email(),
            'price': fake.random_int(min=2500, max=250000),
            'capacity':fake.random_int(min=250, max=60000),
        }
        # Select a random image file from the list
        image_file_name = random.choice(image_files)

        # Create a Django File object from the image file
        with open(os.path.join(image_folder, image_file_name), 'rb') as file:
            django_file = File(file)
            venue_data['picture'] = django_file

        venue_form = VenueForm(data=venue_data)
        if venue_form.is_valid():
            venue = venue_form.save()
            
            # Choose a random user as the manager
 

            # Create an Event instance with fake data and existing manager using EventForm
            event_data = {
                'name': fake.catch_phrase(),
                'event_date': fake.date_time_this_year(),
                'venue': venue.pk,
                'manager': manager,
                'description': fake.paragraph(nb_sentences=25),
                'total_tickets':venue.capacity,
                'available_tickets':venue.capacity,
                'ticket_price' : fake.random_int(min=2500, max=250000),
            }

            event_form = EventForm(data=event_data)
            if event_form.is_valid():
                event = event_form.save()

                # Print the created objects
                print('here are the venue and event')
                print(venue)
                print(event)
            else:
                print(event_form.errors)
        else:
            print('Venue_form errors')
 
            print(venue_form.errors)
if __name__ == "__main__":
    num = int(input('input number of fake date you want to generate'))
    print('populating Scripting')
    fake_date(num)
    print('populating Complete')
