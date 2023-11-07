from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import User
from django.conf import settings


class AppUserManager(BaseUserManager):
	def create_user(self, email, password=None):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		email = self.normalize_email(email)
		user = self.model(email=email)
		user.set_password(password)
		user.save()
		return user
	def create_superuser(self, email, password=None):
		if not email:
			raise ValueError('An email is required.')
		if not password:
			raise ValueError('A password is required.')
		user = self.create_user(email, password)
		user.is_superuser = True
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
    email = models.CharField(max_length=200,)
    driver_license = models.ImageField(upload_to='images/', )
    passport_pic = models.ImageField(upload_to='images/', )
    national_id = models.ImageField(upload_to='images/',)
    car_number = models.CharField(max_length=200, )
    car_picture = models.ImageField(upload_to='images/',)


    def __str__(self):
        return self.name
    