from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserLoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework import authentication, permissions


class Users(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return get_user_model().objects.all()

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = UserSerializer(qs, many=True)
        return Response(serializer.data)


class IsAnonymous(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_anonymous


class CreateUser(APIView):
    """create user and return it with token"""
    permission_classes = [IsAnonymous]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['user_id'] = user.id
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)

            # data : return all data # validated_data : return the only fields that validated
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class LoginUser(APIView):
    permission_classes = [IsAnonymous]

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get('user')
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'email': user.email
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class DetailUpdateUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        ''' only super user and the user itself can see'''
        user = request.user
        uuid = kwargs.get("uuid")
        if not user.is_superuser and user.id != uuid:
            return Response({"error": "Sorry , must be your user !!"}, status=status.HTTP_403_FORBIDDEN)

        qs = get_user_model().objects.filter(id=uuid)
        user = qs.first()
        if user:
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "user Not Found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        ''' only user itself can update'''
        user = request.user
        uuid = kwargs.get("uuid")
        if user.id != uuid:
            return Response({"error": "Sorry , must be your user !!"}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


class DeleteUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        uuid = kwargs.get("uuid")

        if not user.is_superuser and user.id != uuid:
            return Response({"error": "you can't delete the user"}, status=status.HTTP_403_FORBIDDEN)

        qs = get_user_model().objects.filter(id=uuid)
        user = qs.first()
        if user:
            serializer = UserSerializer(user)
            user.delete()
            return Response(serializer.data)

        else:
            return Response({"error": "you can't delete the user"}, status=status.HTTP_403_FORBIDDEN)
