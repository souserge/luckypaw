from django.urls import reverse_lazy, path, include
from . import views
from django.contrib.auth.views import(
    #LoginView,
    LogoutView,
)

urlpatterns = [
    path('', views.index, name='index'),
    path('main/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('search/', views.search, name='search'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('support/', views.support_us, name='support'),
    #path('login/', views.login_site, name='login'),
    #path('logout/', views.index, name='logout'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('index')), name='logout'),
    path('auth/', include('social_django.urls', namespace='social')), 
    path('login/', views.LoginFormView.as_view(), name='login'),
    path('register/', views.RegistrationFormView.as_view(), name='register'),
    path('pet/<id>/', views.pet_profile, name='pet_profile'),
    path('pet/<id>/edit/', views.edit_pet_profile, name='edit_pet_profile'),
    path('user/<username>/', views.user_profile, name='user_profile'),
    path('user/<username>/edit/', views.edit_user_profile, name='edit_user_profile'),

]