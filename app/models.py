from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Pet(models.Model):
    pet_id = models.AutoField(primary_key=True)
    pet_name = models.CharField(max_length=50, default ='No Name', blank=False)
    pet_type_choice = (('Cat','Cat'),('Dog','Dog'),('Parrot','Parrot'))
    pet_type = models.CharField(max_length=50, choices=pet_type_choice, blank=True)
    pet_location = models.CharField(max_length=50, default='', blank=True)
    pet_age_choice = (('Young','Young'),('Adult','Adult'),('Senior','Senior'))
    pet_age = models.CharField(max_length=50, choices=pet_age_choice, blank=True)
    pet_color = models.CharField(max_length=50, default='', blank=True)
    pet_gender_choice = (('Male','Male'),('Female','Female'))
    pet_gender = models.CharField(max_length=50, choices=pet_gender_choice, blank=True)
    pet_size_choice = (('XSmall','XSmall'), ('Small','Small'),('Medium','Medium'),('Large','Large'),('XLarge','XLarge'))
    pet_size = models.CharField(max_length=50, choices=pet_size_choice, blank=True)
    pet_breed = models.CharField(max_length=50, default='', blank=True)
    #pet_needs_choice = (('Spayed/Neutered','Spayed/Neutered'),('Vaccinated','Vaccinated'),('Purebred','Purebred'),('House-trained','House-trained'))
    
        
    def __str__(self):
        return self.pet_name