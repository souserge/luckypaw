from django.contrib.auth.models import User
from . import models
from .filters import PetFilter, PetBaseFilter, PetAdvancedFilter
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView
from .forms import PetForm, PetAddForm, PetAddInfoForm, PhotoForm, AdopterInfoForm
from django.views.generic import FormView
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_GET, require_POST
from django.urls import reverse
from django.views import View
from django.utils.decorators import method_decorator

def pet_list(request):
    pet_list = models.Pet.objects.filter(adopted=False)
    pet_base_filter = PetBaseFilter(request.GET, queryset=pet_list)
    pet_advanced_filter = PetAdvancedFilter(request.GET, queryset=pet_list)
    pets = pet_base_filter.qs & pet_advanced_filter.qs 
    return render(request, 'app/pet_list.html', {'base_filter': pet_base_filter, 
    'advanced_filter': pet_advanced_filter, 'pets': pets })

def pet_list_cards(request):
    pet_list = models.Pet.objects.filter(adopted=False)
    pet_base_filter = PetBaseFilter(request.GET, queryset=pet_list)
    pet_advanced_filter = PetAdvancedFilter(request.GET, queryset=pet_list)
    pets = pet_base_filter.qs & pet_advanced_filter.qs 
    return render(request, 'app/pets_cards.html', {'pets': pets, 'is_supervisor': False })

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
def pet_adopter_info(request, id):
    pet = get_object_or_404(models.Pet, pk=id)
    if(request.user.is_superuser or request.user == pet.supervisor.user):
        return render(request, 'app/pet_adopter_info.html', {'pet': pet})
        
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