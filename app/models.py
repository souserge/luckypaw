from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Pet(models.Model):
    pet_id = models.AutoField(primary_key=True)
    pet_name = models.CharField(max_length=50, default ='', blank=True)
    pet_type_choice = (('Cat','Cat'),('Dog','Dog'),('Parrot','Parrot'))
    pet_type = models.CharField(max_length=50, choices=pet_type_choice, blank=True)
    pet_location = models.CharField(max_length=50, default='', blank=True)
        
    def __str__(self):
        return self.pet_name