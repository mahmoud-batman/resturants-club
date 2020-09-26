from django.contrib import admin
from django.urls import path
from .views import ListRestaurants, SearchRestaurants, DetailRestaurant

urlpatterns = [
    path('', ListRestaurants.as_view()),
    path('<uuid:uuid>/', DetailRestaurant.as_view()),
    path('<slug:slug>/', SearchRestaurants.as_view()),
]
