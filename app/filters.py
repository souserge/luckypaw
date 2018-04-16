from django.contrib.auth.models import User, Group
from django import forms
import django_filters
from .models import Pet

# class UserFilter(django_filters.FilterSet):
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name',]

class PetFilter(django_filters.FilterSet):

    #pet_name = django_filters.CharFilter(name='pet_name', lookup_expr='icontains')
    #pet_type = django_filters.MultipleChoiceFilter(choices=Pet.pet_type_choice, widget=forms.CheckboxSelectMultiple)
    #pet_age = django_filters.MultipleChoiceFilter(choices=Pet.pet_age_choice, widget=forms.CheckboxSelectMultiple)
    #pet_colour = django_filters.CharFilter(name='pet_color', lookup_expr='icontains')
    #pet_gender = django_filters.MultipleChoiceFilter(choices=Pet.pet_gender_choice, widget=forms.CheckboxSelectMultiple)
    #pet_size = django_filters.MultipleChoiceFilter(choices=Pet.pet_size_choice, widget=forms.CheckboxSelectMultiple)
    #pet_breed = django_filters.CharFilter(name='pet_breed', lookup_expr='icontains')
    #pet_spayed = django_filters.BooleanFilter(widget=forms.CheckboxInput)
    #pet_vaccinated = django_filters.BooleanFilter(widget=forms.CheckboxInput)
    #pet_housetrained = django_filters.BooleanFilter(widget=forms.CheckboxInput)
    #pet_specialcare = django_filters.BooleanFilter(widget=forms.CheckboxInput)

    class Meta:
        model = Pet
        fields = ['pet_type', 'pet_location','pet_age','pet_color','pet_gender',
        'pet_spayed','pet_vaccinated','pet_housetrained','pet_specialcare','pet_size','pet_breed']
        