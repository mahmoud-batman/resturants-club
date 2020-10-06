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
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth import get_user_model


class ListCreateRestaurants(APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if not user.is_superuser:
            qs = user.restaurantlocation_set.all()
        else:
            qs = RestaurantLocation.objects.all()
        return qs

    def get(self, request, *args, **kwargs):
        '''authenticated users list there data, superuser list all data'''

        qs = self.get_queryset()
        serializer = RestaurantSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        '''authenticated users can create'''

        serializer = RestaurantSerializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            # .save() will create a new instance.
            serializer.save(owner=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class SearchRestaurants(APIView):

    def get_queryset(self, slug):
        return RestaurantLocation.objects.filter(
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


class DetailUpdateRestaurant(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        uuid = kwargs.get("uuid")
        qs = RestaurantLocation.objects.filter(id=uuid)
        restaurant = qs.first()
        if restaurant:
            serializer = RestaurantSerializer(restaurant)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'restaurant not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        """only owner can update"""

        user = request.user
        uuid = kwargs.get("uuid")
        qs = RestaurantLocation.objects.filter(id=uuid)

        restaurant = qs.first()
        if restaurant:
            if restaurant.owner.id != user.id:
                return Response({"error": "you are not the owner"}, status=status.HTTP_404_NOT_FOUND)
            serializer = RestaurantSerializer(
                restaurant, data=request.data, partial=True)
            if serializer.is_valid():
                # .save() will update an instance.
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

        return Response({'error': 'restaurant not found'}, status=status.HTTP_404_NOT_FOUND)


class DeleteRestaurant(APIView):

    def post(self, request, *args, **kwargs):
        user = request.user
        uuid = kwargs.get("uuid")
        if user.is_superuser:
            qs = RestaurantLocation.objects.filter(id=uuid)
        else:
            qs = user.restaurantlocation_set.filter(id=uuid)
        restaurant = qs.first()
        if restaurant:
            # if not user.is_superuser and user.id != restaurant.owner.id:
            #     return Response({"error": "you can't delete this restaurant"})
            serializer = RestaurantSerializer(restaurant)
            restaurant.delete()
            return Response(serializer.data)
        return Response({"error": "restaurant not found"})
