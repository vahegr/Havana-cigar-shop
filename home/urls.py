from django.urls import path, include, re_path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('about-us', views.about_us_page, name='about_us'),
    path('contact-us', views.contact_us_page, name='contact_us'),
]
