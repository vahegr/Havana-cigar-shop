from django.urls import path, include, re_path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home_page, name='home'),
]
