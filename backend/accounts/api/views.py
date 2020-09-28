from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# from rest_framework import authentication, permissions


class Users(APIView):
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return get_user_model().objects.all()

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = UserSerializer(qs, many=True)
        return Response(serializer.data)


class CreateUser(APIView):
    """create user and return it with token"""

    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.is_anonymous:
            return Response({"error": "you are logged in !!"}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            try:
                email = serializer.validated_data['email']
                user = get_user_model().objects.get(email=email)
                token, created = Token.objects.get_or_create(
                    user=user)
                return Response({'user': serializer.data, 'token': token.key},
                                status=status.HTTP_200_OK)
            except:
                pass
            # data return all data # validated_data return the only fields that validated
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class DetailUpdateUser(APIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self, uuid):
        user = get_user_model().objects.get(id=uuid)
        return user

    def get(self, request, *args, **kwargs):
        ''' only super user and the user itself can see'''
        user = request.user
        uuid = kwargs.get("uuid")
        if not user.is_superuser and user.id != uuid:
            return Response({"error": "Sorry , must be your user !!"}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = self.get_queryset(uuid)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": "user not found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        ''' only user itself can update'''
        user = request.user
        uuid = kwargs.get("uuid")
        if user.id != uuid:
            return Response({"error": "Sorry , must be your user !!"}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = self.get_queryset(uuid)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

        except:
            return Response({"error": "user not found"}, status=status.HTTP_404_NOT_FOUND)


class DeleteUser(APIView):

    def post(self, request, *args, **kwargs):
        user = request.user
        uuid = kwargs.get("uuid")

        if not user.is_superuser and user.id != uuid:
            return Response({"error": "you can't delete the user"}, status=status.HTTP_403_FORBIDDEN)

        try:
            qs = get_user_model().objects.get(id=uuid)
            serializer = UserSerializer(qs)
            qs.delete()
            return Response(serializer.data)

        except:
            return Response({"error": "user not found"})
