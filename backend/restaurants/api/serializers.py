from rest_framework import serializers
from restaurants.models import RestaurantLocation


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = RestaurantLocation
        fields = '__all__'

    # called when save() triggered
    def create(self, validated_data):
        ''' we can override the create method '''
        restaurant = RestaurantLocation.objects.create(**validated_data)
        return restaurant

    # called when save() triggered with the instance
    def update(self, instance, validated_data):
        ''' update or put the exsiting value '''
        instance.name = validated_data.get('name', instance.name)
        instance.location = validated_data.get('location', instance.location)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance
