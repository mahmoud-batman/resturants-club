from django.contrib import admin
from django.urls import path
from .views import ListRestaurants

urlpatterns = [
    path('',ListRestaurants.as_view()),
]
