from rest_framework import serializers
from restaurants.models import RestaurantLocation
from django.contrib.auth import get_user_model
from accounts.api.serializers import UserSerializer


class RestaurantSerializer(serializers.ModelSerializer):

    owner = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = RestaurantLocation
        fields = '__all__'

# use nested serializers instead
    def get_owner(self, obj):
        uuid = obj.owner.id
        owner = get_user_model().objects.get(id=uuid)
        serializer = UserSerializer(owner)
        return serializer.data

    def get_category(self, obj):
        return obj.get_category_display()

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
        # instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance
