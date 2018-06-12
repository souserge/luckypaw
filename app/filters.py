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
    animaltype = django_filters.ChoiceFilter(name='animaltype', label="Animal type")
    location = django_filters.CharFilter(name='location', label='Location', lookup_expr='icontains')
    
    class Meta:
        model = Pet
        fields = ['animaltype', 'location']
        
class PetAdvancedFilter(django_filters.FilterSet):
    breed = django_filters.CharFilter(name='breed', label='Breed', lookup_expr='icontains')
    color = django_filters.CharFilter(name='color', label='Colour', lookup_expr='icontains')
    specialcare = django_filters.ChoiceFilter(name='specialcare', label='Special care')

    class Meta:
        model = Pet
        fields = ['age','color','gender','spayed','vaccinated',
            'housetrained','specialcare','size','breed']