from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'password']
        # extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):  # this happens when is_valid() is called
        if 'gmail' not in value.lower():
            raise serializers.ValidationError("not a gmail")
        return value

    def create(self, validated_data):
        '''Override here when user created'''
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        '''Override here when user updated'''
        instance.email = validated_data.get('email', instance.email)
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(
        trim_whitespace=False,
        write_only=True,
        min_length=8
    )

    def validate_email(self, value):  # field level validation
        if 'gmail' not in value.lower():
            raise serializers.ValidationError("not a gmail")
        return value

    def validate(self, data):  # object level validation
        email = data.get('email')
        password = data.get('password')
        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("User not exists")

        data['user'] = user
        return data
