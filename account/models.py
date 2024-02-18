from django.db import models
from django.contrib.auth.models import AbstractUser

class Currency(models.Model):

    designation = models.CharField(max_length=100)

    def __str__(self):
        return self.designation

class Site(models.Model):
    designation = models.CharField(max_length=100)
    address = models.CharField(max_length=250, null=True)
    prefix_site = models.CharField(max_length=10, blank=True, null=True)
    default_local_currency = models.ForeignKey(Currency, null=True, on_delete=models.SET_NULL, related_name='default_local_currency')
    default_foreign_currency = models.ForeignKey(Currency, null=True, on_delete=models.SET_NULL, related_name='default_foreign_currency')

    def __str__(self):
        return self.designation
    
class User(AbstractUser):

    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    fullname = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)
    sites = models.ManyToManyField(Site, blank=True)

    fields = ('username', 'fullname', 'email', 'is_admin', 'first_name', 'last_name', 'sites')
    
    def __str__(self):
        return self.fullname

    class Meta(AbstractUser.Meta):
       swappable = 'AUTH_USER_MODEL'