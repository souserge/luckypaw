from django.db import models
from django.contrib.auth.models import User
import os
from django.core.files.storage import default_storage
from django.db.models import FileField
from django.db import models
from django.db.models.signals import post_delete


def pet_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/pets/id_<id>/<filename>
    return 'pets/id_{0}/{1}'.format(instance.id, filename)

def article_directory_path(filename):
    # file will be uploaded to MEDIA_ROOT/users/id_<id>/<filename>
    return 'articles/{1}'.format(filename)

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/users/id_<id>/<filename>
    return 'users/id_{0}/{1}'.format(instance.user.id, filename)

# def file_cleanup(sender, **kwargs):
#     for fieldname in sender._meta.get_all_field_names():
#         try:
#             field = sender._meta.get_field(fieldname)
#         except:
#             field = None
#             if field and isinstance(field, FileField):
#                 inst = kwargs['instance']
#                 f = getattr(inst, fieldname)
#                 m = inst.__class__._default_manager
#                 if hasattr(f, 'path') and os.path.exists(f.path)\
#                 and not m.filter(**{'%s__exact' % fieldname: getattr(inst, fieldname)})\
#                 .exclude(pk=inst._get_pk_val()):
#                         try:
#                             default_storage.delete(f.path)
#                         except:
#                             pass

# Create your models here.


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
    # photo = models.ImageField(upload_to=pet_directory_path, default='pets/pet_default_image.jpg')
    description = models.CharField(max_length=2000, default='', blank=True)
    # gallery = models.OneToOneField(Gallery, related_name='pet_gallery', on_delete=models.SET_NULL, blank=True, null=True)
    spayed = models.NullBooleanField()
    vaccinated = models.NullBooleanField()
    housetrained = models.NullBooleanField()
    specialcare = models.NullBooleanField()
    adopted = models.NullBooleanField(default=False)

    # One-to-Many relationship (one Supervisor can have multiple pets) 
    # When a referenced object deleted, set FK to null
    supervisor = models.ForeignKey(Supervisor, on_delete=models.SET_NULL, blank=True, null=True)


    @property
    def photo(self):
        first_photo = Photo.objects.filter(pet=self).first()
        return first_photo.image if first_photo is not None else {'url': '/media/pets/pet_default_image.jpg' }

    def __str__(self):
        return self.name

    #post_delete.connect(file_cleanup, sender=photo, dispatch_uid=pet_directory_path)

User.supervisor = property(lambda u: Supervisor.objects.get_or_create(user=u)[0])
# Pet.photo = property(lambda p: Pet.objects.get_or_create(pet=p[0]))
