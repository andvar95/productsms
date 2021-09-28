from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class Products(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    category = models.CharField(max_length=200)
    discount = models.DecimalField(decimal_places=5, max_digits=10)
    quantity = models.IntegerField(default=10)
    in_stock = models.BooleanField()


class Preferences(models.Model):
    user = models.IntegerField()
    preferences = ArrayField(models.IntegerField())