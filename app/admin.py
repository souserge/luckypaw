from django.contrib import admin
from .models import Supervisor, Pet, Photo

# Register your models here.

class SuperAdmin(admin.ModelAdmin):
    list_display = ["user", "city", "country", "telephone"]

    class Meta:
        model = Supervisor

class PetAdmin(admin.ModelAdmin):
    list_display = ["name", "animaltype", "location", "age", "color", "gender", "size", "breed",
        "spayed", "vaccinated", "housetrained", "adopted", "specialcare"]

    class Meta:
        model = Pet

admin.site.register(Supervisor, SuperAdmin)
admin.site.register(Pet, PetAdmin)
admin.site.register(Photo)
