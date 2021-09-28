from django.db import models
from numpy import product
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Products
from .helpers.recommendation import createDataset,addProduct




class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('id', 'name','description','price','category','discount','quantity','in_stock')

