from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model
from .serializers import UserSerializer

# from rest_framework import authentication, permissions


class Users(APIView):

    def get_queryset(self):
        return get_user_model().objects.all()

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = UserSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
            # data return all data # validated_data return the only fields that validated
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class DetailUser(APIView):

    def get_queryset(self, uuid):
        user = get_user_model().objects.get(id=uuid)
        return user

    def get(self, request, *args, **kwargs):
        uuid = kwargs.get("uuid")
        try:
            user = self.get_queryset(uuid)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": "user not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        uuid = kwargs.get("uuid")
        try:
            user = self.get_queryset(uuid)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

        except:
            return Response({"error": "user not found"}, status=status.HTTP_404_NOT_FOUND)
