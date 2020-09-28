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
        owner = kwargs.get("owner")
        return RestaurantLocation.objects.filter(owner=owner)

    def get(self, request, *args, **kwargs):
        '''authenticated users list there data, superuser list all data'''

        user = request.user
        if not user.is_superuser:
            qs = self.get_queryset(owner=user)
        else:
            qs = RestaurantLocation.objects.all()
        serializer = RestaurantSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        '''authenticated users can create'''

        serializer = RestaurantSerializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            # .save() will create a new instance.
            serializer.save(owner=user)
            return Response(serializer.validated_data)
        return Response(serializer.errors)


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
        try:
            restaurant = RestaurantLocation.objects.get(
                id=uuid)
            serializer = RestaurantSerializer(restaurant)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except RestaurantLocation.DoesNotExist:
            content = {'error': 'restaurant not found'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        """only owner can update"""

        uuid = kwargs.get("uuid")
        user = request.user
        try:
            restaurant = RestaurantLocation.objects.get(id=uuid)
            serializer = RestaurantSerializer(
                restaurant, data=request.data, partial=True)
            # partial=True , allow partial updates for required fields.
            if restaurant.owner.id != user.id:
                return Response({"error": "you are not the owner"}, status=status.HTTP_404_NOT_FOUND)
            if serializer.is_valid():
                # .save() will update an instance.
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        except RestaurantLocation.DoesNotExist:
            return Response({'error': 'restaurant not found'}, status=status.HTTP_404_NOT_FOUND)


class DeleteRestaurant(APIView):

    def post(self, request, *args, **kwargs):
        user = request.user
        uuid = kwargs.get("uuid")
        try:
            restaurant = RestaurantLocation.objects.get(id=uuid)
            if not user.is_superuser and user.id != restaurant.owner.id:
                return Response({"error": "you can't delete this restaurant"})
            serializer = RestaurantSerializer(restaurant)
            restaurant.delete()
            return Response(serializer.data)
        except:
            return Response({"error": "restaurant not found"})
