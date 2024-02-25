from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.core import validators
from account.models import User
from .models import Order, OrderItem, Product


class OrderCreationForm(forms.ModelForm):
    email_address = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control", 'placeholder': 'Email Address'}))
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Full Name'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Phone Number'}))
    city = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'City'}))
    zip_code = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Zip Code'}))
    post_code = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Post Code'}))
    details_text = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control", 'placeholder': 'More Details'}))

    class Meta:
        model = Order
        fields = ('name', 'email_address', 'phone_number', 'city', 'zip_code', 'post_code', 'details_text')
