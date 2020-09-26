from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from restaurants.models import RestaurantLocation
from .serializers import RestaurantSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response


class ListRestaurants(APIView):

    def get_queryset(self, *args, **kwargs):
        return RestaurantLocation.objects.all()

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = RestaurantSerializer(qs, many=True)
        return Response(serializer.data)


class SearchRestaurants(APIView):

    def get_queryset(self, slug):
        return RestaurantLocation.objects.filter(  # filter return QuerySet not object like get()
            Q(name__icontains=slug) |
            Q(name__iexact=slug) |
            Q(slug__icontains=slug) |
            Q(slug__iexact=slug) |
            Q(location__iexact=slug) |
            Q(category__iexact=slug)
        )

    def get(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        qs = self.get_queryset(slug)
        if qs.exists():
            serializer = RestaurantSerializer(qs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "NO result"}, status=status.HTTP_404_NOT_FOUND)


class DetailRestaurant(APIView):

    def get(self, request, *args, **kwargs):
        uuid = kwargs.get("uuid")
        try:
            restaurant = RestaurantLocation.objects.get(
                id=uuid)  # get return object not QuerySet like filter()
            serializer = RestaurantSerializer(restaurant)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except RestaurantLocation.DoesNotExist:
            content = {'error': 'not found'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
