from django.contrib import admin
from django.urls import path
from .views import ListCreateRestaurants, SearchRestaurants, DetailUpdateRestaurant, DeleteRestaurant

urlpatterns = [
    path('', ListCreateRestaurants.as_view()),
    path('<uuid:uuid>/', DetailUpdateRestaurant.as_view()),
    path('<uuid:uuid>/delete/', DeleteRestaurant.as_view()),
    path('<slug:slug>/', SearchRestaurants.as_view()),
]
