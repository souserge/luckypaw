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
from django.db.models import Q

from django.core.mail import send_mail, BadHeaderError

def index(request):
    if request.user.is_authenticated:
        sup = get_object_or_404(models.Supervisor, user=request.user)
        pets = models.Pet.objects.filter(supervisor__user=request.user)
        context = {
            'supervisor': sup,
            'all_pets': pets,
            'unadopted_pets': pets.filter(adopted=False),            
            'adopted_pets': pets.filter(adopted=True),
        }
        return render(request, 'app/sup_pets.html', context)    
    return render(request, 'app/index.html')

def about(request):
    return render(request, 'app/about.html')

def search(request):
    return render(request, 'app/search.html')

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
    query = request.GET.get("q")
    if query:
        articles = models.Article.objects.filter(Q(title__icontains=query) | Q(body__icontains=query)).distinct() 
    else:
        articles = models.Article.objects.all()
    
    featured = request.GET.get("f")
    if featured:
        articles = articles.filter(featured=True)

    return render(request, 'app/blog.html', { 'articles': articles })

def featured_articles(request):
    articles = models.Article.objects.filter(featured=True)
    num_feat = articles.count()
    if num_feat > 3:
        articles = articles[:3]

    return render(request, 'app/featured_articles.html', { 'feat_articles': articles })

def article(request, id):
    article = get_object_or_404(models.Article, id=id)
    article.view_count += 1
    article.save()
    return render(request, 'app/article.html', { 'article': article })

def support_us(request):
    return render(request, 'app/support_us.html')

def thank_you(request):
    return render(render, 'app/thank_you.html')

def user_profile(request, username):
    user = User.objects.get(username=username)
    supervisor = get_object_or_404(models.Supervisor, user=user) 
    pets = models.Pet.objects.filter(supervisor__user=user, adopted=False)
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

class LoginFormView(FormView):
    form_class = LoginForm
    template_name = 'app/user_login.html'
    def get(self, request, *args, **kwargs):
        login_form = LoginForm()
        register_form = RegistrationForm()
        response = self.get_context_data(register_form=register_form, login_form=login_form)
        return self.render_to_response(response)


def login_form(request, *args, **kwargs):
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            raw_password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login_supervisor(request, user)
            if request.is_ajax():
                return HttpResponse(reverse('index'))

            return redirect('index')
        elif request.is_ajax():
            return JsonResponse(login_form.errors, status=400)

    login_form = LoginForm()
    return render(request, 'app/login.html', {'form': login_form })

def register(request):
    if request.method == 'POST':
        register_form = RegistrationForm(data=request.POST)
        if register_form.is_valid():
            register_form.save()
            username = register_form.cleaned_data.get('username')
            raw_password = register_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login_supervisor(request, user)
            if request.is_ajax():
                return HttpResponse(reverse('index'))

            return redirect('index')
        elif request.is_ajax():
            return JsonResponse(register_form.errors, status=400)

    register_form = RegistrationForm()
    return render(request, 'app/register.html', { 'form': register_form })


def login_supervisor(request, user):
    sup, created = models.Supervisor.objects.get_or_create(user=user)
    if created:
        print("created")
        sup.user = user
        sup.save()
    else:
        print("not created")

    login(request, user)