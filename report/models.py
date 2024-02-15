from django.db import models
from account.models import User, Site
from django.core.validators import MinValueValidator, MaxValueValidator

class Emplacement(models.Model):
 
    REGION = [
        ('Ouest', 'Ouest'),
        ('Est', 'Est'),
        ('Centre', 'Centre'),
        ('Centre/Ouest', 'Centre/Ouest'),
    ]

    designation = models.CharField(max_length=100)
    region = models.CharField(choices=REGION, max_length=20, default='Ouest')

    def __str__(self):
        return self.designation

class Transitor(models.Model):

    designation = models.CharField(max_length=100)

    def __str__(self):
        return self.designation

class Currency(models.Model):

    designation = models.CharField(max_length=100)

    def __str__(self):
        return self.designation

class Report(models.Model):
 
    STATE_REPORT = [
        ('Brouillon', 'Brouillon'),
        ('Confirmé', 'Confirmé'),
        ('Annulé', 'Annulé'),
    ]

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    state = models.CharField(choices=STATE_REPORT, max_length=40)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True)


    fournisseur_id = models.IntegerField(blank=True, null=True)
    fournisseur = models.CharField(max_length=255, blank=True, null=True)

    n_facture = models.CharField(max_length=15, blank=True, null=True)
    lieu_decharge = models.ForeignKey(Emplacement, null=True, on_delete=models.SET_NULL)
    transitor = models.ForeignKey(Transitor, null=True, on_delete=models.SET_NULL)
    n_facture2 = models.CharField(max_length=15, blank=True, null=True)
    camion = models.IntegerField(null=True)
    date_in_stock = models.DateField()
    date_calc_cost = models.DateField()
    exchange_rate = models.FloatField(default=1, validators=[MinValueValidator(0)])

    facture_amount = models.FloatField(default=0, validators=[MinValueValidator(0)])
    facture_amount_currency = models.ForeignKey(Currency, null=True, on_delete=models.SET_NULL, related_name='facture_amount_currency')
    facture_fees = models.FloatField(default=0, validators=[MinValueValidator(0)])
    facture_fees_currency = models.ForeignKey(Currency, null=True, on_delete=models.SET_NULL, related_name='facture_fees_currency')
    ladding_bill = models.FloatField(default=0, validators=[MinValueValidator(0)])
    ladding_bill_currency = models.ForeignKey(Currency, null=True, on_delete=models.SET_NULL, related_name='ladding_bill_currency')
    shopping = models.FloatField(default=0, validators=[MinValueValidator(0)])
    shopping_currency = models.ForeignKey(Currency, null=True, on_delete=models.SET_NULL, related_name='shopping_currency')
    customs = models.FloatField(default=0, validators=[MinValueValidator(0)])
    tcs = models.FloatField(default=0, validators=[MinValueValidator(0)])
    tcs_currency = models.ForeignKey(Currency, null=True, on_delete=models.SET_NULL, related_name='tcs_currency')
    dd = models.FloatField(default=0, validators=[MinValueValidator(0)])
    dd_currency = models.ForeignKey(Currency, null=True, on_delete=models.SET_NULL, related_name='dd_currency')
    customs_honorary = models.FloatField(default=0, validators=[MinValueValidator(0)])



   
    n_report = models.IntegerField()
    n_lot = models.IntegerField(null=True)
    date_prelev = models.DateTimeField()
    variateur = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    debit =  models.FloatField(default=0, validators=[MinValueValidator(0)])
    t_consigne =  models.FloatField(default=0)
    t_real =  models.FloatField(default=0)
    freq_b1 =  models.FloatField(default=0)
    variateur_b1 =  models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    freq_b2 =  models.FloatField(default=0)
    variateur_b2 =  models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    freq_b3 =  models.FloatField(default=0, null=True, blank=True)
    variateur_b3 =  models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], null=True, blank=True)
    retour_2_5 = models.BooleanField(default=True)
    retour_1_3 = models.BooleanField(default=True)
    retour_0_6 = models.BooleanField(default=True)
    observation = models.TextField(null=True, blank=True)
    
    def validations(self):
        return self.validation_set.all()
    
    def samples(self):
        return self.sample_set.all()
    
    def __str__(self):
        return str(self.n_report) + " (" + str(self.date_created) +")"