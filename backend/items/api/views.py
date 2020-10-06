from rest_framework.views import APIView
from rest_framework.response import Response
from restaurants.models import RestaurantLocation
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib.auth import get_user_model
from rest_framework import status

from items.models import Item
from .serializers import ItemSerializer
import uuid
import re


UUID_PATTERN = re.compile(
    r'^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$', re.IGNORECASE)


def is_valid_uuid(uuid):
    if UUID_PATTERN.match(str(uuid)):
        return True
    else:
        return False


class ListCreateItem(APIView):
    permission_classes = [IsAuthenticated]

    def restaurant_queryset(self, user, restaurant_uuid):
        if user.is_superuser:  # filter over all Restaurants
            qs = RestaurantLocation.objects.filter(
                id=restaurant_uuid)
        else:  # filter over user's restaurants
            qs = user.restaurantlocation_set.filter(
                id=restaurant_uuid)
        return qs

    def get(self, request, *args, **kwargs):
        ''' list items '''
        user = request.user
        if user.is_superuser:
            qs = Item.objects.all()
        else:
            qs = user.item_set.all()

        item = qs.first()
        if item:
            serializer = ItemSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        restaurant_uuid = request.data.get("restaurant")
        if not is_valid_uuid(restaurant_uuid):
            return Response({"error": "Invalid Restaurant UUID"}, status=status.HTTP_404_NOT_FOUND)
        qs = self.restaurant_queryset(user, restaurant_uuid)
        restaurant = qs.first()
        if restaurant:
            serializer = ItemSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(owner=user, restaurant=restaurant)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "restaurant not found"}, status=status.HTTP_404_NOT_FOUND)


class DetailUpdateItem(APIView):
    permission_class = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        item_uuid = kwargs.get("uuid")
        user = request.user
        item_qs = self.item_queryset(user, item_uuid)
        item = item_qs.first()
        if item:
            serializer = ItemSerializer(item)
            return Response(serializer.data)
        else:
            return Response({"error": "wrong uuid"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        user = request.user
        item_uuid = kwargs.get("uuid")
        restaurant_uuid = request.data.get("restaurant")

        if restaurant_uuid and not is_valid_uuid(restaurant_uuid):
            return Response({"error": "Invalid UUID"}, status=status.HTTP_404_NOT_FOUND)

        if restaurant_uuid:
            restaurant_qs = self.restaurant_queryset(user, restaurant_uuid)
            restaurant = restaurant_qs.first()
            if not restaurant:
                return Response({"error": "you can't add to this restaurant"}, status=status.HTTP_404_NOT_FOUND)

        if item_uuid:
            item_qs = self.item_queryset(user, item_uuid)
            item = item_qs.first()
            if not item:
                return Response({"error": "you can't update to this item"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def restaurant_queryset(self, user, restaurant_uuid):
        if user.is_superuser:  # filter over all Restaurants
            qs = RestaurantLocation.objects.filter(
                id=restaurant_uuid)
        else:  # filter over user's restaurants
            qs = user.restaurantlocation_set.filter(
                id=restaurant_uuid)
        return qs

    def item_queryset(self, user, item_uuid):
        if user.is_superuser:
            qs = Item.objects.filter(id=item_uuid)
        else:
            qs = user.item_set.filter(id=item_uuid)
        return qs


class DeleteItem(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        item_uuid = kwargs.get("uuid")
        if user.is_superuser:
            qs = Item.objects.filter(id=uuid)
        else:
            qs = user.item_set.filter(id=uuid)
        item = qs.first()
        if item:
            serializer = ItemSerializer(item)
            item.delete()
            return Response(serializer.data)
        return Response({"error": "restaurant not found"})
