from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from restaurants.models import RestaurantLocation
from .serializers import ListRestaurantSerializer
# from rest_framework import generics

class ListRestaurants(APIView):
    def get(self,request, *args,**kwargs):
        qs = RestaurantLocation.objects.all()
        serializer = ListRestaurantSerializer(qs, many=True)
        print(serializer.data)
        return Response(serializer.data)