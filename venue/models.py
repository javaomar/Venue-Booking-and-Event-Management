from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
User = get_user_model()
import random

from django.template.defaultfilters import slugify
import os
 
from django.utils import timezone
import misaka 

# Create your models here.
def random_default_picture():
	# Get the list of files in the 'default' folder
	default_folder = os.path.join('media', 'default')
	default_pics = [os.path.join(default_folder, filename) for filename in os.listdir(default_folder)]

	# Choose a random default picture
	picture = random.choice(default_pics)
	return picture


def upload_image_to(instance, filename):
    # Use the slugified name of the venue as part of the filename
    slug = slugify(instance.slug)
    return os.path.join('venue_images', slug, filename)

class Venue(models.Model):
	name = models.CharField('Venue Name', max_length=120)
	owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE,related_name='owned_venues')
	address = models.CharField(max_length=300)
	slug = models.SlugField('Series slug', null=True, blank=True, unique=True)
	zip_code = models.CharField('Zip Code', max_length=15)
	phone = models.CharField('Contact Phone', max_length=25, blank=True)
	web = models.URLField('Website Address', blank=True)
	descriptions = models.TextField(blank=True, null=True)
	email_address = models.EmailField('Email Address', max_length=40, blank=True)
	price = models.PositiveIntegerField(default=0)
	capacity = models.PositiveIntegerField(blank=True, null=True)  
	#profie pic for venue 
	picture = models.ImageField(upload_to=upload_image_to,default=random_default_picture, blank=True)

	def save(self, *args, **kwargs):
		# Generate the slug from the name field if not provided
		if not self.slug:
			self.slug = slugify(self.name)
		super(Venue, self).save(*args, **kwargs)

	def __str__(self):
		return self.name
	class Meta: 
		ordering = ['name']
		unique_together = ['name','owner']


 
 



