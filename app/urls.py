from django.urls import reverse_lazy, path, include
from . import views
from . import pet_views
from django.contrib.auth.views import(
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
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('index')), name='logout'),
    path('auth/', include('social_django.urls', namespace='social')), 
    path('login/', views.login_form, name='login'),
    path('login-register-modal/', views.LoginFormView.as_view(), name='login_register_modal'),
    path('register/', views.register, name='register'),
    path('pets/', pet_views.pet_list, name='pet_list'),
    path('pets/cards', pet_views.pet_list_cards, name='pet_list_cards'),
    path('pet/add/', pet_views.pet_add, name='pet_add'),
    path('pet/<id>/add_info/', pet_views.pet_add_info, name='pet_add_info'),
    path('pet/<id>/', pet_views.pet_profile, name='pet_profile'),
    path('pet/<id>/edit/', pet_views.pet_edit, name='pet_edit'),
    path('pet/<id>/delete/', pet_views.pet_delete, name='pet_delete'),
    path('pet/<id>/upload_photo/', pet_views.pet_upload_photo, name='pet_upload_photo'),
    path('pet/<id>/delete_photo/', pet_views.pet_delete_photo, name='pet_delete_photo'),
    path('pet/<id>/adopt/', pet_views.pet_adopt, name='pet_adopt'),
    path('pet/<id>/unadopt/', pet_views.pet_unadopt, name='pet_unadopt'),    
    path('pet/<id>/adopter/', pet_views.pet_adopter_info, name='pet_adopter_info'),        
    path('user/<username>/', views.user_profile, name='user_profile'),
    path('user/<username>/edit/', views.user_edit, name='user_edit'),
    path('article/<id>/', views.article, name='article'),
    path('article/<id>/', views.article, name='article'),
]