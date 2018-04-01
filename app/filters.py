from django.contrib.auth.models import User
import django_filters
from .models import Pet

# class UserFilter(django_filters.FilterSet):
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name',]

class PetFilter(django_filters.FilterSet):

    # pet_name = django_filters.CharFilter(name='pet_name', lookup_expr='icontains')

    class Meta:
        model = Pet
        fields = ['pet_name', 'pet_type']
        