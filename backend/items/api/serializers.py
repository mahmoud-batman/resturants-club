from rest_framework import serializers
from items.models import Item


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ["id", "name", "contents", "excludes", "restaurant"]

    def create(self, validated_data, *args, **kwargs):
        return Item.objects.create(**validated_data)

    def update(self, instance, validated_data):
        ''' update or put the exsiting value '''
        instance.name = validated_data.get('name', instance.name)
        instance.contents = validated_data.get('contents', instance.contents)
        instance.excludes = validated_data.get('excludes', instance.excludes)
        instance.restaurant = validated_data.get(
            'restaurant', instance.restaurant)
        instance.save()
        return instance
