from django.contrib.auth.models import User
from . import models
from .filters import PetFilter, PetBaseFilter, PetAdvancedFilter
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView
from .forms import RegistrationForm, LoginForm, PetForm, UserForm, SupervisorForm, PetAddForm, PetAddInfoForm, PhotoForm, ContactForm, AdopterInfoForm
from django.views.generic import FormView
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_GET, require_POST
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator

from django.core.mail import send_mail, BadHeaderError

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
    if request.user.is_authenticated:
        sup = get_object_or_404(models.Supervisor, user=request.user)
        sup_pets = models.Pet.objects.filter(supervisor__user=request.user)
        return render(request, 'app/sup_pets.html', { 'supervisor': sup, 'pets': sup_pets })    
    return render(request, 'app/index.html')

def about(request):
    return render(request, 'app/about.html')

def search(request):
    pet_list = models.Pet.objects.all()
    pet_base_filter = PetBaseFilter(request.GET, queryset=pet_list)
    pet_advanced_filter = PetAdvancedFilter(request.GET, queryset=pet_list)
    pets = pet_base_filter.qs & pet_advanced_filter.qs 
    return render(request, 'app/pet_list.html', {'base_filter': pet_base_filter, 
    'advanced_filter': pet_advanced_filter, 'pets': pets })

def contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():

            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['name'] + '\n' + form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['serge@korzh.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponse('Success! Thank you for your message.')
    return render(request, "app/contact.html", {'form': form})

def blog(request):
    articles = models.Article.objects.all()
    return render(request, 'app/blog.html', { 'articles': articles })

def article(request, id):
    article = get_object_or_404(models.Article, id=id)
    article.view_count += 1
    article.save()
    return render(request, 'app/article.html', { 'article': article })

def support_us(request):
    return render(request, 'app/support_us.html')

def thank_you(request):
    return render(render, 'app/thank_you.html')

def login_site(self, request, *args, **kwargs):
    login_form = LoginForm(self.request.GET or None)
    register_form = RegistrationForm(self.request.GET or None)
    context = self.get_context_data(**kwargs)
    context['login_form'] = login_form
    context['register_form'] = register_form
    return self.render_to_response(context)

@login_required
def user_profile(request, username):
    user = User.objects.get(username=username)
    supervisor = get_object_or_404(models.Supervisor, user=user) 
    pets = models.Pet.objects.filter(supervisor__user=user)
    return render(request, 'app/user_profile.html', {'supervisor': supervisor, 'user': user, 'pets': pets})

@login_required
def user_edit(request, username):
    if request.method == 'POST':
        user = User.objects.get(username=username)
        if(request.user.is_superuser or request.user == user):
            supervisor = get_object_or_404(models.Supervisor, user=user)
            user_form = UserForm(request.POST, instance=user) 
            supervisor_form = SupervisorForm(request.POST, request.FILES, instance=supervisor)
            if user_form.is_valid() and supervisor_form.is_valid():
                user_form.save(commit=True)
                supervisor_form.save(commit=True)
                return redirect('user_profile', username=username)
            else:
                return render(request, 'app/user_edit.html', {'user_form': user_form, 'supervisor_form' : supervisor_form})
        else:
            return redirect('user_profile', username=username)
    else:
        user = User.objects.get(username=username)
        if(request.user.is_superuser or request.user == user):
            supervisor = get_object_or_404(models.Supervisor, user=user)
            user_form = UserForm(instance=user) 
            supervisor_form = SupervisorForm(instance=supervisor)
            return render(request, 'app/user_edit.html', {'user_form': user_form, 'supervisor_form' : supervisor_form})
        else:
            return redirect('user_profile', username=username)

def pet_profile(request, id):
    pet = models.Pet.objects.get(id=id)
    return render(request, 'app/pet_profile.html', {'pet': pet, 'supervisor': pet.supervisor})

@login_required
def pet_add(request):
    if request.method == 'POST':
        pet_form = PetAddForm(request.POST)
        if pet_form.is_valid():
            pet = pet_form.save(commit=False)
            # User who creates new pet become his supervisor automatically
            supervisor = get_object_or_404(models.Supervisor, user=request.user)
            pet.supervisor = supervisor
            pet_form.save(commit=True)
            id = pet.id
            return redirect('pet_add_info', id=id)
    else:
        pet_form = PetAddForm
        return render(request, 'app/pet_add.html', {'pet_form': pet_form })

# @login_required
# def pet_add_info(request, id):
#     if request.method == 'POST':
#         pet = get_object_or_404(models.Pet, pk=id)
#         pet_info_form = PetAddInfoForm(request.POST, request.FILES, instance=pet)
#         if pet_info_form.is_valid():
#             pet_info_form.save(commit=True)
#             # return redirect('index')
#             return redirect('pet_upload_photo', id=id)
#     else:
#         pet = get_object_or_404(models.Pet, pk=id)
#         pet_info_form = PetAddInfoForm(instance=pet)
#         return render(request, 'app/pet_add_info.html', {'pet_info_form': pet_info_form})



@login_required
def pet_add_info(request, id):
    if request.method == 'POST':
        pet = get_object_or_404(models.Pet, pk=id)
        pet_info_form = PetAddInfoForm(request.POST, instance=pet)

        if pet_info_form.is_valid():
            pet_info_form.save(commit=True)  
            return redirect('index')
    
    else:
        pet = get_object_or_404(models.Pet, pk=id)
        pet_info_form = PetAddInfoForm(instance=pet)
        return render(request, 'app/pet_add_info_test.html', {'pet_info_form': pet_info_form,
        'photos' : pet.photos, 'id' : id})


@require_POST
def pet_upload_photo(request, id):
    print("Hi, Hi")
    form = PhotoForm(request.POST, request.FILES)
    if form.is_valid():
        pet = get_object_or_404(models.Pet, pk=id)
        photo = form.save(commit=False)
        photo.pet = pet
        form.save(commit=True)
        data = {'is_valid': True, 'pet_id': id, 'name': photo.image.name, 'url': photo.image.url}
    else:
        data = {'is_valid': False}
    return JsonResponse(data)


@require_POST
def pet_delete_photo(request, id):
    photo_name = request.POST['name']
    photo = models.Photo.objects.get(pet__id=id, image_name=photo_name)
    photo.delete()
    return JsonResponse({status: 302 })




@login_required
def pet_edit(request, id):
    pet = get_object_or_404(models.Pet, pk=id)
    if(request.user.is_superuser or request.user == pet.supervisor.user):
        if request.method == 'POST':
            pet_form = PetForm(request.POST, request.FILES, instance=pet)
            if pet_form.is_valid():
                pet_form.save(commit=True)
                return redirect('pet_profile', id=id)
        else:
            pet_form = PetForm(instance=pet)
        return render(request, 'app/pet_edit.html', {'pet_form': pet_form, 'id': id, 'pet': pet})
    else:
        return redirect('pet_profile', id=id)

@login_required
def pet_adopt(request, id):
    pet = get_object_or_404(models.Pet, pk=id)
    if(request.user.is_superuser or request.user == pet.supervisor.user):
        if request.method == 'POST':
            form = AdopterInfoForm(request.POST)
            if form.is_valid():
                adopter_info = form.save()
                pet.adopter_info = adopter_info
                pet.adopted = True
                pet.save()
                return redirect('index')
        else:
            form = AdopterInfoForm(instance=pet.adopter_info) 

        return render(request, 'app/pet_adopt.html', {'form': form, 'pet': pet, 'id': id})
    
    return redirect('index')

@login_required
def pet_unadopt(request, id):
    pet = get_object_or_404(models.Pet, pk=id)
    if(request.user.is_superuser or request.user == pet.supervisor.user):
        if request.method == 'POST':
            pet.adopted = False
            pet.save()         
            return HttpResponse(reverse('pet_edit', args=[id]))
    return redirect('index')

@login_required
def pet_delete(request, id):
    pet = get_object_or_404(models.Pet, pk=id)
    if(request.user.is_superuser or request.user == pet.supervisor.user):
        if request.method == 'POST':
            pet.delete()
            return redirect('index')
        else:            
            return render(request, 'app/pet_delete.html', {'pet': pet, 'id': id})
    else:
        return redirect('index')

class LoginFormView(FormView):
    form_class = LoginForm
    template_name = 'app/user_login.html'
    def get(self, request, *args, **kwargs):
        login_form = LoginForm()
        register_form = RegistrationForm()
        response = self.get_context_data(register_form=register_form, login_form=login_form)
        return self.render_to_response(response)


@require_POST
def login_form(request, *args, **kwargs):
    login_form = LoginForm(data=request.POST)
    if login_form.is_valid():
        username = login_form.cleaned_data.get('username')
        raw_password = login_form.cleaned_data.get('password')
        user = authenticate(username=username, password=raw_password)
        login(request, user)
        return HttpResponse(reverse('index'))
    else:
        return JsonResponse(login_form.errors, status=400)

@require_POST
def register(request):
    register_form = RegistrationForm(data=request.POST)
    if register_form.is_valid():
        register_form.save()
        username = register_form.cleaned_data.get('username')
        raw_password = register_form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(request, user)
        return HttpResponse(reverse('index'))
    else:
        return JsonResponse(register_form.errors, status=400)


# @method_decorator(login_required, name='post')
# class PhotoUploadView(View):
#     form_class = PhotoForm

#     def get(self, request, id, *args, **kwargs):
#         pet = get_object_or_404(models.Pet, pk=id)
#         photos_list = models.Photo.objects.all().filter(pet=pet)
#         return render(request, 'app/pet_upload_photo.html', {'photos' : photos_list, 'id' : id})
#         # return render(self.request, '', {'photos': photos_list})


#     def post(self, request, id, *args, **kwargs) :
#         pet = get_object_or_404(models.Pet, pk=id)
#         form = PhotoForm(self.request.POST, self.request.FILES)
#         if form.is_valid():
#             photo = form.save()
#             data = {'is_valid': True, 'name': photo.image.name, 'url': photo.image.url}
#         else:
#             data = {'is_valid': False}
#         return JsonResponse(data)


# @login_required
# def pet_add_info(request, id):
#     if request.method == 'POST':
#         pet = get_object_or_404(models.Pet, pk=id)
#         form = PhotoForm(request.POST, request.FILES, instance=pet)
#     if form.is_valid():
#             photo = form.save()
#             data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
#         else:
#             data = {'is_valid': False}
#         return JsonResponse(data)
#     else:
#         pet = get_object_or_404(models.Pet, pk=id)
#         photos_list = models.Photo.objects.all().filter(pet=pet)
#         return render(request, 'app/pet_upload_photo.html', {'photos' : photos_list})