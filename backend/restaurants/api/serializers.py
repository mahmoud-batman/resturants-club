from rest_framework import serializers
from restaurants.models import RestaurantLocation

class ListRestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = RestaurantLocation
        fields = "__all__"