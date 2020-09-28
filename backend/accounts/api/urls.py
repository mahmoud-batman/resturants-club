from django.contrib import admin
from django.urls import path, include
from .views import Users, DetailUpdateUser, CreateUser, DeleteUser

urlpatterns = [
    path('', Users.as_view()),
    path('create/', CreateUser.as_view()),
    path('<uuid:uuid>/', DetailUpdateUser.as_view()),
    path('<uuid:uuid>/delete', DeleteUser.as_view()),
]
