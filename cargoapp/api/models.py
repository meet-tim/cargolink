from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import User
from django.conf import settings


class AppUserManager(BaseUserManager):
	def create_user(self, email,username, password=None):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		email = self.normalize_email(email)
		user = self.model(email=email)
		user.set_password(password)
		user.save()
		return user
	def create_superuser(self, email,username, password=None,):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		user = self.create_user(email, password,username)
		user.is_superuser = True
		user.is_staff = True
		user.save()
		return user

USER_TYPE_CHOICES = (
        ('driver', 'Driver'),
        ('passenger', 'Passenger'),
    )

class AppUser(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=50, unique=True)
    username = models.CharField(max_length=50)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='passenger')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = AppUserManager()
    def __str__(self):
    	return self.username
    


    
class Driver(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200, )
    lastname =  models.CharField(max_length=200,)
    phone = models.PositiveIntegerField(max_length=200, )
    driver_license = models.CharField(max_length=200)
    passport_pic = models.CharField(max_length=200)
    national_id = models.CharField(max_length=200)
    car_number = models.CharField(max_length=200, )
    car_picture = models.CharField(max_length=200, )
    car_space = models.PositiveIntegerField(max_length=100)


    def __str__(self):
        return self.name
    

class Trip (models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='trips_offered',null=True)
    departure_location = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    departure_time = models.DateTimeField()
    
    space_left = models.PositiveIntegerField(max_length=5000,default=5000)
    created_at = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return f"Trip from {self.departure_location} to {self.destination}"

    class Meta:
        ordering = ['-departure_time']
		
class Booking (models.Model):
	passenger = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	trip = models.ForeignKey(Trip,on_delete=models.CASCADE)
	phone = models.PositiveIntegerField(max_length=200, )
	full_name = models.CharField(max_length=100)
	id_number = models.CharField(max_length=100)
	cargo_size = models.PositiveIntegerField(max_length=100)
	