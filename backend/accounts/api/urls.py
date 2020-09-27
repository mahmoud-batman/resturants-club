from django.contrib import admin
from django.urls import path, include
from .views import Users, DetailUser

urlpatterns = [
    path('', Users.as_view()),
    path('<uuid:uuid>/', DetailUser.as_view()),
]
