from django.contrib.auth.models import User
from .models import Pet
# from .filters import UserFilter 
from .filters import PetFilter
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.base import TemplateView

# Create your views here.

to_be_continued = """
This is the main page of Lucky Paw - a service aimed at helping homless
animals find their ideal owners.
At the moment, nothing special is here. In fact, it is not even an
HTML page, just an HTTP response.
But do not worry, in a few Sprints, it will be both functional, and
beautiful! See You soon ~~
"""

about_us = """
The web portal "Lucky Paw" was established by group of students
in order to help homeless pets to find their new home
There are still more information to add ...
(⌐ ͡■ ͜ʖ ͡■) 
"""

def index(request):
    return render(request, 'app/index.html')

def about(request):
    return render(request, 'app/about.html')

# def search(request):
#     return render(request, 'app/search.html')

# def search(request):
#     user_list = User.objects.all()
#     user_filter = UserFilter(request.GET, queryset=user_list)
#     return render(request, 'app/user_list.html', {'filter': user_filter})

def search(request):
    pet_list = Pet.objects.all()
    pet_filter = PetFilter(request.GET, queryset=pet_list)
    return render(request, 'app/pet_list.html', {'filter': pet_filter})

def contact(request):
    return render(request, 'app/contact.html')
