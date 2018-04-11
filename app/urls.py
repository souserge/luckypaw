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
    path('login/', views.login_site, name='login'),
    #path('logout/', views.index, name='logout'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('index')), name='logout'),
    path('auth/', include('social_django.urls', namespace='social')), 
]