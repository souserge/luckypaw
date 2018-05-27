from django.contrib.auth.models import User, Group
from django import forms
import django_filters
from .models import Pet

class PetFilter(django_filters.FilterSet):
    
    class Meta:
        model = Pet
        fields = ['animaltype', 'location','age','color','gender',
        'spayed','vaccinated','housetrained','specialcare','size','breed']
        

class PetBaseFilter(django_filters.FilterSet):
    
    class Meta:
        model = Pet
        fields = ['animaltype', 'location']
        
class PetAdvancedFilter(django_filters.FilterSet):
    
    class Meta:
        model = Pet
        fields = ['age','color','gender','spayed','vaccinated',
        'housetrained','specialcare','size','breed']