from django.db import models
from django.contrib.auth.models  import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
 
	STATUS = (
	    ('regular', 'regular'),
	    ('moderator', 'moderator'),
	)

	email = models.EmailField(unique=True)
	status = models.CharField(max_length=100, choices=STATUS, default='regular')
	  
	def __str__(self):
	    return self.username

# class User(auth.models.User,auth.models.PermissionsMixin):

# 	def __str__(self):
# 		return "@{}".format(self.username)

# 	class Meta:
# 		ordering = ['last_name']