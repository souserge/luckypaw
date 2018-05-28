from django.db import models
from django.contrib.auth.models import User
import os
from django.core.files.storage import default_storage
from django.db.models import FileField
from django.db import models
from django.db.models.signals import post_delete
from django.conf import settings


def pet_directory_path(instance, filename):
    return 'pets/{0}'.format(filename)

def article_directory_path(instance, filename):
    return 'articles/{0}'.format(filename)

def user_directory_path(instance, filename):
    return 'users/{0}'.format(filename)


# Picture of the gallery
class Photo(models.Model):
    pet = models.ForeignKey('Pet', on_delete=models.CASCADE, blank=True, null=True)
    image = models.FileField(upload_to=pet_directory_path, default='pets/pet_default_image.jpg')


class Supervisor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    city = models.CharField(max_length=50, default='', blank=True)
    country = models.CharField(max_length=50, default='', blank=True)
    telephone = models.CharField(max_length=50, default='', blank=True)
    photo = models.ImageField(upload_to=user_directory_path, default='users/user_default_image.jpg')
    description = models.CharField(max_length=2000, default='', blank=True)

    def __str__(self):
        return self.user.username

class AdopterInfo(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, default='', blank=False)
    last_name = models.CharField(max_length=50, default='', blank=True)
    location = models.CharField(max_length=50, default='', blank=False)
    email = models.CharField(max_length=50, default='', blank=False)
    phone_number = models.CharField(max_length=50, default='', blank=False)
    date_adopted = models.DateField(auto_now=True)

    @property
    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, default='', blank=True)
    body = models.TextField()
    author = models.CharField(max_length=50, default='', blank=True)
    photo = models.ImageField(upload_to=article_directory_path, default='articles/article_default_image.jpg')
    date_published = models.DateField(auto_now=True)
    view_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Pet(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False)
    animaltype_choice = (('Cat','Cat'),('Dog','Dog'),('Parrot','Parrot'))
    animaltype = models.CharField(max_length=50, choices=animaltype_choice, blank=False)
    location = models.CharField(max_length=50, default='', blank=False)
    age_choice = (('Young','Young'),('Adult','Adult'),('Senior','Senior'))
    age = models.CharField(max_length=50, choices=age_choice, blank=True)
    color = models.CharField(max_length=50, default='', blank=True)
    gender_choice = (('Male','Male'),('Female','Female'))
    gender = models.CharField(max_length=50, choices=gender_choice, blank=True)
    size_choice = (('Very Small','Very Small'), ('Small','Small'),('Medium','Medium'),('Large','Large'),('Very Large','Very Large'))
    size = models.CharField(max_length=50, choices=size_choice, blank=True)
    breed = models.CharField(max_length=50, default='', blank=True)
    description = models.CharField(max_length=2000, default='', blank=True)
    spayed = models.NullBooleanField()
    vaccinated = models.NullBooleanField()
    housetrained = models.NullBooleanField()
    specialcare = models.NullBooleanField()
    adopted = models.NullBooleanField(default=False)
    adopter_info = models.ForeignKey(AdopterInfo, on_delete=models.SET_NULL, blank=True, null=True)

    # One-to-Many relationship (one Supervisor can have multiple pets) 
    # When a referenced object deleted, set FK to null
    supervisor = models.ForeignKey(Supervisor, on_delete=models.SET_NULL, blank=True, null=True)


    @property
    def photo(self):
        photos = self.photos
        return photos[0] if (len(photos) > 0) else self.default_photo

    @property
    def default_photo(self):
        return { 'name': 'default-pet-photo', 'url': settings.MEDIA_URL + Photo._meta.get_field('image').default }

    @property
    def photos(self):
        return [photo.image for photo in Photo.objects.filter(pet=self)]

    def __str__(self):
        return self.name


User.supervisor = property(lambda u: Supervisor.objects.get_or_create(user=u)[0])