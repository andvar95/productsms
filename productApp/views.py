from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework.decorators import action
from .models import Products,Preferences
from .serializers import ProductSerializers
from rest_framework import response, serializers, viewsets
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend, filterset
from django.forms.models import model_to_dict
import json
from .helpers.recommendation import createDataset,addProduct,generateSimilarityMatrix,get_important_features,modifySimilarityMatrix

# Create your views here.

class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name','price','category','in_stock']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        addProduct(serializer.data,)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        get_important_features()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if request.GET.get('user'):
            ids = modifySimilarityMatrix(serializer.data['name'])
            try:
                preferences = Preferences.objects.get(user=request.GET.get('user'))
                preferences.preferences = ids
                preferences.save()
            except:
                preferences = Preferences.objects.create(preferences=ids, user =request.GET.get('user') )
                preferences.save()
        return response.Response(serializer.data)


    @action(detail=False, methods=['GET'],name="recommendations")
    def recommendations(self,request,pk=None):        
        userPreferences = Preferences.objects.get(user=request.GET.get('user'))
        products = []
        for id in userPreferences.preferences:
            prod = Products.objects.get(pk=id)
            products.append(prod)
        serializers = self.get_serializer(products,many=True)
        return response.Response(serializers.data,status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST','GET'],name="checkstock")
    def checkstock(self,request,pk=None):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        error={}
        productsToSave = []
        for bodyProduct in body:
            product = model_to_dict(Products.objects.get(pk=bodyProduct['id']))
            if bodyProduct['quantity']>product['quantity']:
                error[product['name']] = "Exceso en {} unidades".format(bodyProduct['quantity']-product['quantity'])
            elif len(error)==0:
                product['quantity'] -= bodyProduct['quantity']
                productsToSave.append(product)

        if len(error)==0:
            for prToSave in productsToSave:
                product = Products.objects.get(pk=prToSave['id'])
                product.quantity = prToSave['quantity']
                product.save()

            return response.Response({"status":'Ok'},status=status.HTTP_200_OK)
            
        return response.Response(error,status=status.HTTP_409_CONFLICT)
     
