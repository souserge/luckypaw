from django.contrib.auth.models import User
from .models import Pet
# from .filters import UserFilter 
from .filters import PetFilter
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from .forms import RegistrationForm, LoginForm
from django.views.generic import FormView
from django.contrib.auth import login, authenticate

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

def search(request):
    pet_list = Pet.objects.all()
    pet_filter = PetFilter(request.GET, queryset=pet_list)
    return render(request, 'app/pet_list.html', {'filter': pet_filter})

def contact(request):
    return render(request, 'app/contact.html')

def blog(request):
    return render(request, 'app/blog.html')

def support_us(request):
    return render(request, 'app/support_us.html')

# def login_site(request):
#     return render(request, 'app/login.html')

def login_site(self, request, *args, **kwargs):
    login_form = LoginForm(self.request.GET or None)
    context = self.get_context_data(**kwargs)
    context['login_form'] = login_form
    return self.render_to_response(context)


class RegistrationFormView(FormView):
    form_class = RegistrationForm
    template_name = 'app/user_register.html'

    def get(self, request, *args, **kwargs):
        register_form = self.form_class()
        return self.render_to_response(
            self.get_context_data(
                register_form=register_form,
            )
        )


    def post(self, request, *args, **kwargs):
        register_form = self.form_class(request.POST)
        if register_form.is_valid():
            register_form.save()
            username = register_form.cleaned_data.get('username')
            raw_password = register_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
        else:
            return self.render_to_response(
            self.get_context_data(
                register_form=register_form,
            )
        )


class LoginFormView(FormView):
    form_class = LoginForm
    template_name = 'app/user_login.html'

    def get(self, request, *args, **kwargs):
        login_form = self.form_class()

        return self.render_to_response(
            self.get_context_data(
                login_form=login_form
            )
        )

    def post(self, request, *args, **kwargs):
        login_form = self.form_class(data=request.POST)

        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            raw_password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
        else:
            return self.render_to_response(
            self.get_context_data(
                    login_form=login_form,
            )
        )
