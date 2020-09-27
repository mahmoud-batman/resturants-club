from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'is_staff', 'timestamp', 'updated']

    def validate_email(self, value):  # this happens when is_valid() is called
        if 'gmail' not in value.lower():
            raise serializers.ValidationError("not a gmail")
        return value

    def create(self, validated_data):
        '''Override here when user created'''
        return get_user_model().objects.create(**validated_data)

    def update(self, instance, validated_data):
        '''Override here when user updated'''
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance
