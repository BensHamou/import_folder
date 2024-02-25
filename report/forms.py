from django.forms import ModelForm, inlineformset_factory
from django import forms
from .models import *
from account.models import *
from django.utils import timezone
from django.db.models import Q


def getAttrs(type, placeholder='', other={}):
    ATTRIBUTES = {
        'control': {'class': 'form-control', 'style': 'background-color: #e0e5f5;', 'placeholder': ''},
        'controlReq': {'class': 'form-control', 'autocomplete': "off", 'style': 'background-color: #dad2ff; border-color: #dad2ff;', 'placeholder': ''},
        'controlIDReq': {'class': 'form-control search-input-id', 'autocomplete': "off", 'style': 'background-color: #dad2ff; border-color: #dad2ff;', 'placeholder': ''},
        'controlIDTDReq': {'class': 'form-control search-input-id-td', 'autocomplete': "off", 'style': 'background-color: #dad2ff; border-color: #dad2ff;', 'placeholder': ''},
        'search': {'class': 'form-control form-input', 'style': 'background-color: rgba(202, 207, 215, 0.5); box-shadow: 0 0 6px rgba(0, 0, 0, 0.2); color: #45558a; height: 40px; text-indent: 33px; border-radius: 5px;', 'type': 'search', 'placeholder': '', 'id': 'search'},
        'controlSearchReq': {'class': 'form-control search-input', 'autocomplete': "off", 'style': 'background-color: #dad2ff; border-color: #dad2ff;', 'placeholder': ''},
        'controlSearchTDReq': {'class': 'form-control search-input-td', 'autocomplete': "off", 'style': 'background-color: #dad2ff; border-color: #dad2ff;', 'placeholder': ''},
        'select': {'class': 'form-select', 'style': 'background-color: #e0e5f5;'},
        'selectReq': {'class': 'form-select', 'style': 'background-color: #dad2ff; border-color: #dad2ff;'},
        'select2': {'class': 'form-select custom-select', 'style': 'background-color: #e0e5f5; width: 100%;'},
        'select2Req': {'class': 'form-select custom-select', 'style': 'background-color: #dad2ff; border-color: #dad2ff; width: 100%;'},
        'date': {'type': 'date', 'class': 'form-control dateinput','style': 'background-color: #e0e5f5;'},
        'dateReq': {'type': 'date', 'class': 'form-control dateinput', 'style': 'background-color: #dad2ff; border-color: #dad2ff;'},
        'datetime': {'type': 'datetime-local', 'class': 'form-control dateinput','style': 'background-color: #dad2ff; border-color: #dad2ff; '},
        'textarea': {"rows": "3", 'style': 'width: 100%', 'class': 'form-control', 'placeholder': '', 'style': 'background-color: #e0e5f5;'}
    }

    
    if type in ATTRIBUTES:
        attributes = ATTRIBUTES[type]
        if 'placeholder' in attributes:
            attributes['placeholder'] = placeholder
        if other:
            attributes.update(other)
            attributes
        return attributes
    else:
        return {}
    
class EmplacementForm(ModelForm):
    class Meta:
        model = Emplacement
        fields = ['designation', 'region']
    
    designation = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control','Désignation')))
    region = forms.ChoiceField(choices=Emplacement.REGION, widget=forms.Select(attrs=getAttrs('select')))
       
class TransitorForm(ModelForm):
    class Meta:
        model = Transitor
        fields = ['designation']

    designation = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control', 'Désignation')))

class BudgetCostForm(ModelForm):
    class Meta:
        model = BudgetCost
        fields = ['article_id', 'article_code', 'article_designation', 'budget']

    min = {'min': '0', 'step': '0.001'}

    article_code = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlSearchReq','Code')))
    article_designation = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlReq','Designation', {'disabled': 'disabled'})))
    article_id = forms.IntegerField(widget=forms.HiddenInput(attrs=getAttrs('controlIDReq','ID_article_id')))
    budget = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('controlReq','Budget', min)))

    def clean(self):
        cleaned_data = super().clean()
        article_code = cleaned_data.get('article_code')

        if article_code:
            if self.instance.pk:
                existing_budget = BudgetCost.objects.filter(article_code=article_code).exclude( Q(id=self.instance.pk)).first()
            else:
                existing_budget = BudgetCost.objects.filter(article_code=article_code).first()
            if existing_budget:
                self.add_error('article_code', f'Un coût budgutaire pour ce produit existe déjà. (id = {existing_budget.id})')
        return cleaned_data

class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ['ref_folder', 'site', 'fournisseur', 'fournisseur_id', 'n_facture', 'lieu_decharge', 'transitor', 'n_facture2', 
                  'camion', 'date_in_stock', 'date_calc_cost', 'exchange_rate', 'facture_amount', 'facture_fees', 'facture_currency', 
                  'ladding_bill', 'shopping', 'customs', 'tcs', 'daps', 'dd', 'customs_honorary', 'local_transport', 'other_fees', 'surestaries'
                  , 'local_currency', 'observation']

    # n_report = forms.IntegerField(widget=forms.NumberInput(attrs= getAttrs('controlReq','N° Rapport')))
    ref_folder = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlReq','N° de dossier')))

    site = forms.ModelChoiceField(queryset=Site.objects.all(), widget=forms.Select(attrs= getAttrs('select2')), empty_label="Site")

    fournisseur = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlSearchReq','Fournisseur')))
    n_facture = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlReq', 'N° Facture')))
    lieu_decharge = forms.ModelChoiceField(queryset=Emplacement.objects.all(), widget=forms.Select(attrs= getAttrs('select2Req')), empty_label="Lieu Déchargement")
    transitor = forms.ModelChoiceField(queryset=Transitor.objects.all(), widget=forms.Select(attrs= getAttrs('select2Req')), empty_label="Transitaire")
    n_facture2 = forms.CharField(widget=forms.TextInput(attrs=getAttrs('control', 'N° Facture 2')), required=False)
    camion = forms.IntegerField(widget=forms.NumberInput(attrs= getAttrs('controlReq','Camion')))
    date_in_stock = forms.DateField(initial=timezone.now().date(), widget=forms.widgets.DateInput(attrs= getAttrs('dateReq'), format='%Y-%m-%d'))
    date_calc_cost = forms.DateField(initial=timezone.now().date(), widget=forms.widgets.DateInput(attrs= getAttrs('dateReq'), format='%Y-%m-%d'))

    exchange_rate = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('controlReq','Taux de Cahnge')))
    facture_amount = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('controlReq','Montant Facture')))
    facture_fees = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('controlReq','Montant Fret')))
    facture_currency = forms.ModelChoiceField(queryset=Currency.objects.all(), widget=forms.Select(attrs= getAttrs('selectReq')), empty_label="Devise")

    ladding_bill = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('controlReq','Connaissement')))
    shopping = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('controlReq','Magasinage')))
    customs = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('controlReq','Douanes Algerienne')))
    local_currency = forms.ModelChoiceField(queryset=Currency.objects.all(), widget=forms.Select(attrs= getAttrs('selectReq')), empty_label="Devise")

    tcs = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','TCS')), required=False)
    daps = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','DAPS')), required=False)
    dd = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('control','DD')), required=False)
    
    customs_honorary = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('controlReq','Honorraire Douanes')))
    local_transport = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('controlReq','Transport Local')))
    other_fees = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('controlReq','Autres Frais')))
    surestaries = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('controlReq','Serustaries')))

    observation = forms.CharField(widget=forms.Textarea(attrs= getAttrs('textarea','Observation')), required=False)

    fournisseur_id = forms.IntegerField(widget=forms.HiddenInput(attrs=getAttrs('controlIDReq','ID_fournisseur_id')))


    def __init__(self, *args, **kwargs):
        admin = kwargs.pop('admin', None)
        sites = kwargs.pop('sites', None)
        state = kwargs.pop('state', None)
        super(ReportForm, self).__init__(*args, **kwargs)
        if sites is not None:
            self.fields['site'].queryset = sites
            site = sites.first()
            if site:
                self.fields['site'].initial = site
                self.fields['facture_currency'].initial = site.default_foreign_currency
                self.fields['local_currency'].initial = site.default_local_currency
            if not admin and len(sites) < 2:
                self.fields['site'].widget.attrs['disabled'] = True
    
    # def clean(self):
    #     cleaned_data = super().clean()
    #     n_report = cleaned_data.get('n_report')
    #     site = cleaned_data.get('site')
    #     date_in_stock = cleaned_data.get('date_in_stock')

    #     if n_report and n_report != 0 and site:
    #         if self.instance.pk:
    #             existing_report = Report.objects.filter(n_report=n_report, site=site, date_in_stock__year=date_in_stock.year).exclude( Q(id=self.instance.pk) | Q(state='Annulé')).exists()
    #         else:
    #             existing_report = Report.objects.filter(n_report=n_report, site=site, date_in_stock__year=date_in_stock.year).exclude(state='Annulé').exists()
    #         if n_report and n_report != 0 and site:
    #             if existing_report:
    #                 self.add_error('n_report', 'Un rapport avec ce numéro existe déjà pour ce site.')
    #     return cleaned_data
    
class PImportedForm(ModelForm):
    class Meta:
        model = PImported
        fields = ['article_id', 'article_code', 'article_designation', 'qte', 'prix_exw', 'tcs', 'dd', 'daps', 'nbr_blt', 'repartition']
    
    min_max = {'max': '100', 'min': '0', 'step': '0.001'}
    min = {'min': '0', 'step': '0.001'}

    article_code = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlSearchTDReq','Code')))
    article_designation = forms.CharField(widget=forms.TextInput(attrs=getAttrs('controlReq','Designation', {'disabled': 'disabled'})))
    article_id = forms.IntegerField(widget=forms.HiddenInput(attrs=getAttrs('controlIDTDReq','ID_fournisseur_id')))
    qte = forms.FloatField(widget=forms.NumberInput(attrs= getAttrs('controlReq','Quantité', min)))
    prix_exw = forms.FloatField(label='Prix EXW', widget=forms.NumberInput(attrs= getAttrs('controlReq','Prix EXW', min)))
    tcs = forms.FloatField(label='TCS', widget=forms.NumberInput(attrs= getAttrs('control','TCS', min_max)), required=False)
    dd = forms.FloatField(label='DD', widget=forms.NumberInput(attrs= getAttrs('control','DD', min)), required=False)
    daps = forms.FloatField(label='DAPS', widget=forms.NumberInput(attrs= getAttrs('control','DAPS', min)), required=False)
    
    nbr_blt = forms.IntegerField(label='Nombre Palletes', widget=forms.NumberInput(attrs= getAttrs('controlReq','Nombre Pallete')))
    repartition = forms.FloatField(label='Répartition', widget=forms.NumberInput(attrs= getAttrs('controlReq','Répartition', min)))

PImportedsFormSet = inlineformset_factory(Report, PImported, form=PImportedForm, 
                                          fields=['article_code', 'article_designation', 'article_id', 'qte', 'prix_exw', 
                                                  'tcs', 'dd', 'daps', 'nbr_blt', 'repartition'], extra=0)
