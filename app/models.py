from django.db import models
from django.contrib.auth.models import User


def pet_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/pets/id_<id>/<filename>
    return 'pets/id_{0}/{1}'.format(instance.id, filename)

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/users/id_<id>/<filename>
    return 'users/id_{0}/{1}'.format(instance.user.id, filename)


# Create your models here.

class Gallery(models.Model):
    title = models.CharField(max_length=50)


# Picture of the gallery
class Picture(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=pet_directory_path, default='pets/pet_default_image.jpg')


class Supervisor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    city = models.CharField(max_length=50, default='', blank=True)
    country = models.CharField(max_length=50, default='', blank=True)
    telephone = models.CharField(max_length=50, default='', blank=True)
    photo = models.ImageField(upload_to=user_directory_path, default='users/user_default_image.jpg')
    description = models.CharField(max_length=2000, default='', blank=True)

    def __str__(self):
        return self.user.username


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
    photo = models.ImageField(upload_to=pet_directory_path, default='pets/pet_default_image.jpg')
    description = models.CharField(max_length=2000, default='', blank=True)
    gallery = models.OneToOneField(Gallery, related_name='pet_gallery', on_delete=models.SET_NULL, blank=True, null=True)
    spayed = models.BooleanField()
    vaccinated = models.BooleanField()
    housetrained = models.BooleanField()
    specialcare = models.BooleanField()

    # One-to-Many relationship (one Supervisor can have multiple pets) 
    # When a referenced object deleted, set FK to null
    supervisor = models.ForeignKey(Supervisor, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name

User.supervisor = property(lambda u: Supervisor.objects.get_or_create(user=u)[0])