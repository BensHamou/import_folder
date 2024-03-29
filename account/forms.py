from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from report.forms import getAttrs

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'fullname', 'email', 'is_admin', 'first_name', 'last_name', 'sites']

    attr = {'class': 'form-control', 'style': 'background-color: #cacfd7;', 'readonly':'readonly'}

    username = forms.CharField(widget=forms.TextInput(attrs=attr))
    last_name = forms.CharField(widget=forms.TextInput(attrs=attr))
    first_name = forms.CharField(widget=forms.TextInput(attrs=attr))
    fullname = forms.CharField(widget=forms.TextInput(attrs=attr))
    email = forms.EmailField(widget=forms.EmailInput(attrs=attr))
    sites = forms.SelectMultiple(attrs={'class': 'form-select'})
    is_admin = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'type': 'checkbox', 'data-onstyle':'secondary', 'data-toggle':'switchbutton'}))
   
class CurrencyForm(ModelForm):
    class Meta:
        model = Currency
        fields = ['designation']

    designation = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control', 'Désignation')))
class SiteForm(ModelForm):
    class Meta:
        model = Site
        fields = ['designation', 'address', 'prefix_site', 'default_local_currency', 'default_foreign_currency']

    designation = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control', 'Désignation')))
    address = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control', 'Address')))
    prefix_site = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control', 'Préfixe')))
    default_local_currency = forms.ModelChoiceField(queryset=Currency.objects.all(), widget=forms.Select(attrs= getAttrs('select')), empty_label="Devise Locale Par Défault")
    default_foreign_currency = forms.ModelChoiceField(queryset=Currency.objects.all(), widget=forms.Select(attrs= getAttrs('select')), empty_label="Devise Étrangère Par Défault")

class CustomLoginForm(AuthenticationForm):
    style = 'height: 45px; color: black; border: none; border-bottom: 1px solid black;'
    username = forms.CharField( label="Email / AD 2000", widget=forms.TextInput(attrs={'autofocus': True, 'style': style, 'class': 'form-control', 'placeholder':'Adresse e-mail'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Mot de passe', 'style': style}))
 
 