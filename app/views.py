from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

to_be_continued = """
This is the main page of Lucky Paw - a service aimed at helping homless
animals find their ideal owners.
At the moment, nothing special is here. In fact, it is not even an
HTML page, just an HTTP response.
But do not worry, in a few Sprints, it will be both functional, and
beautiful! See You soon ^_^
"""


def index(request):
    return HttpResponse(to_be_continued)