from django.db import models
from account.models import User, Site
from django.core.validators import MinValueValidator, MaxValueValidator

class Setting(models.Model):
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=250)

    def __str__(self):
        return self.name + ' : ' + self.value

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

    n_report = models.IntegerField()

    fournisseur_id = models.IntegerField()
    fournisseur = models.CharField(max_length=255)

    n_facture = models.CharField(max_length=15)
    lieu_decharge = models.ForeignKey(Emplacement, null=True, on_delete=models.SET_NULL)
    transitor = models.ForeignKey(Transitor, null=True, on_delete=models.SET_NULL)
    n_facture2 = models.CharField(max_length=15, blank=True, null=True)
    camion = models.IntegerField()
    date_in_stock = models.DateField()
    date_calc_cost = models.DateField()
    
    exchange_rate = models.FloatField(default=1, validators=[MinValueValidator(0)])
    facture_amount = models.FloatField(default=0, validators=[MinValueValidator(0)])
    facture_fees = models.FloatField(default=0, validators=[MinValueValidator(0)])
    facture_currency = models.ForeignKey(Currency, null=True, on_delete=models.SET_NULL, related_name='facture_currency')
    
    ladding_bill = models.FloatField(default=0, validators=[MinValueValidator(0)])
    local_currency = models.ForeignKey(Currency, null=True, on_delete=models.SET_NULL, related_name='local_currency')
    shopping = models.FloatField(default=0, validators=[MinValueValidator(0)])
    customs = models.FloatField(default=0, validators=[MinValueValidator(0)])
    tcs = models.FloatField(default=0, validators=[MinValueValidator(0)], null=True)
    daps = models.FloatField(default=0, validators=[MinValueValidator(0)], null=True)
    dd = models.FloatField(default=0, validators=[MinValueValidator(0)], null=True)
    customs_honorary = models.FloatField(default=0, validators=[MinValueValidator(0)])
    local_transport = models.FloatField(default=0, validators=[MinValueValidator(0)])
    other_fees = models.FloatField(default=0, validators=[MinValueValidator(0)])
    surestaries = models.FloatField(default=0, validators=[MinValueValidator(0)])
    
    observation = models.TextField(null=True, blank=True)

    @property
    def total(self):
        tcs = self.tcs or 0
        daps = self.daps or 0
        dd = self.dd or 0
        return ( (self.facture_amount + self.facture_fees) * self.exchange_rate + self.ladding_bill + self.shopping + 
                self.customs + tcs + daps + dd + self.customs_honorary + self.local_transport + self.other_fees + self.surestaries)

    @property
    def total_products_qte(self):
        return sum([product.qte for product in self.pimported_set.all()])

    @property
    def total_products_fret(self):
        return sum([product.fret for product in self.pimported_set.all()])

    @property
    def total_products_dzd(self):
        return sum([product.dzd for product in self.pimported_set.all()])

    @property
    def total_products_mnt_tcs(self):
        return sum([product.mnt_tcs for product in self.pimported_set.all()])

    @property
    def total_products_mnt_dd(self):
        return sum([product.mnt_dd for product in self.pimported_set.all()])

    @property
    def total_products_mnt_daps(self):
        return sum([product.mnt_daps for product in self.pimported_set.all()])

    @property
    def total_products_mnt_diver(self):
        return sum([product.mnt_diver for product in self.pimported_set.all()])

    @property
    def total_products_total(self):
        return sum([product.total for product in self.pimported_set.all()])

    @property
    def total_products_nbr_plt(self):
        return sum([product.nbr_blt for product in self.pimported_set.all()])

    @property
    def total_products_repartition(self):
        return sum([product.repartition for product in self.pimported_set.all()])
    
    @property
    def gap(self):
        return self.total - self.total_products_total
    
    def pimporteds(self):
        return self.pimported_set.all()
    
    def __str__(self):
        return str(self.n_report) + " (" + str(self.date_created) +")"
    
class PImported(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    article_id = models.IntegerField(blank=True, null=True)
    article_code = models.CharField(max_length=255, blank=True, null=True)
    article_designation = models.CharField(max_length=255, blank=True, null=True)
    qte = models.FloatField(default=0, validators=[MinValueValidator(0)])
    prix_exw = models.FloatField(default=0, validators=[MinValueValidator(0)])
    tcs = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    dd = models.FloatField(default=0, validators=[MinValueValidator(0)])
    daps = models.FloatField(default=0, validators=[MinValueValidator(0)])
    
    nbr_blt = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    repartition = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])


    @property
    def local_currency(self):
        return self.report.local_currency


    @property
    def foreign_currency(self):
        return self.report.facture_currency


    @property
    def fret(self):
        return self.repartition * self.report.facture_fees
    
    @property
    def dzd(self):
        return ((self.qte * self.prix_exw) + self.fret)  * self.report.exchange_rate
    
    @property
    def mnt_tcs(self):
        return self.tcs  * self.dzd
    
    @property
    def mnt_dd(self):
        return self.dd  * self.dzd
    
    @property
    def mnt_daps(self):
        return self.daps  * self.dzd
    
    @property
    def mnt_diver(self):
        return (self.report.customs_honorary + self.report.local_transport + self.report.other_fees + self.report.surestaries + 
                self.report.ladding_bill + self.report.shopping + self.report.customs) * self.repartition
    
    @property
    def total(self):
        return (self.dzd + self.mnt_tcs + self.mnt_dd + self.mnt_daps + self.mnt_diver) * self.repartition
    
    @property
    def cost_u(self):
        return self.qte * self.total

    def __str__(self):
        return self.article_code + self.article_designation + " - " + self.repartition + "% (R" + str(self.report.id) +")"