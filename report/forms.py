from django.forms import ModelForm, inlineformset_factory
from django import forms
from .models import *
from account.models import *
from django.utils import timezone
from django.db.models import Q


def getAttrs(type, placeholder='', other={}):
    ATTRIBUTES = {
        'control': {'class': 'form-control', 'style': 'background-color: #e0e5f5;', 'placeholder': ''},
        'search': {'class': 'form-control form-input', 'style': 'background-color: rgba(202, 207, 215, 0.5); box-shadow: 0 0 6px rgba(0, 0, 0, 0.2); color: #45558a; height: 40px; text-indent: 33px; border-radius: 5px;', 'type': 'search', 'placeholder': '', 'id': 'search'},
        'select': {'class': 'form-select', 'style': 'background-color: #e0e5f5;'},
        'select2': {'class': 'form-select custom-select', 'style': 'background-color: #e0e5f5; width: 100%;'},
        'date': {'type': 'date', 'class': 'form-control dateinput','style': 'background-color: #e0e5f5;'},
        'datetime': {'type': 'datetime-local', 'class': 'form-control dateinput','style': 'background-color: #e0e5f5;'},
        'textarea': {"rows": "3", 'style': 'width: 100%', 'class': 'form-control', 'placeholder': '', 'style': 'background-color: #e0e5f5;'}
    }

    
    if type in ATTRIBUTES:
        attributes = ATTRIBUTES[type]
        if 'placeholder' in attributes:
            attributes['placeholder'] = placeholder
        if other:
            attributes.update(other)
        return attributes
    else:
        return {}
