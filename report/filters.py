import django_filters
from django_filters import ChoiceFilter, CharFilter, ModelChoiceFilter, FilterSet, DateTimeFilter
from django import forms
from .forms import getAttrs
from .models import *
from django.db.models import Q

class EmplacementFilter(FilterSet):

    search = CharFilter(method='filter_search', widget=forms.TextInput(attrs=getAttrs('search', 'Rechercher Emplacement..')))

    def filter_search(self, queryset, name, value):
        return queryset.filter( Q(designation__icontains=value) | Q(region__icontains=value) ).distinct()

    class Meta:
        model = Emplacement
        fields = ['search']

class TransitorFilter(FilterSet):

    search = CharFilter(method='filter_search', widget=forms.TextInput(attrs=getAttrs('search', 'Rechercher Transitaire..') ))

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(designation__icontains=value)).distinct()

    class Meta:
        model = Transitor
        fields = ['search']

class BudgetCostFilter(FilterSet):

    search = CharFilter(method='filter_search', widget=forms.TextInput(attrs=getAttrs('search', 'Rechercher Coût Budgetaire..') ))

    def filter_search(self, queryset, name, value):
        return queryset.filter(Q(article_code__icontains=value) | Q(article_designation__icontains=value)).distinct()

    class Meta:
        model = Transitor
        fields = ['search']

class ReportFilter(FilterSet):

    other = {'style': 'background-color: rgba(202, 207, 215, 0.5); box-shadow: 0 0 6px rgba(0, 0, 0, 0.2); color: #45558a; height: 40px; border-radius: 5px;'}
    
    search = CharFilter(method='filter_search', widget=forms.TextInput(attrs=getAttrs('search', 'Rechercher..')))
    state = ChoiceFilter(choices=Report.STATE_REPORT, widget=forms.Select(attrs=getAttrs('select')), empty_label="État")
    start_date = DateTimeFilter(field_name='date_in_stock', lookup_expr='gte', widget=forms.widgets.DateTimeInput(format=('%Y-%m-%dT%H:%M'), attrs= getAttrs('datetime', other=other)))
    end_date = DateTimeFilter(field_name='date_in_stock', lookup_expr='lte', widget=forms.widgets.DateTimeInput(format=('%Y-%m-%dT%H:%M'), attrs= getAttrs('datetime', other=other)))
    site = ModelChoiceFilter(queryset=Site.objects.all(), widget=forms.Select(attrs= getAttrs('select', other=other)), empty_label="Site")

    def filter_search(self, queryset, name, value):
        return queryset.filter( Q(n_report__icontains=value) | Q(creator__fullname__icontains=value) | Q(fournisseur__icontains=value)
                               | Q(lieu_decharge__designation__icontains=value) | Q(transitor__designation__icontains=value) ).distinct()

    class Meta:
        model = Report
        fields = ['search', 'state', 'start_date', 'end_date', 'site']
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ReportFilter, self).__init__(*args, **kwargs)
        if user:
            self.filters['site'].queryset = user.sites.all()

