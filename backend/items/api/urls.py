from django.urls import path
from .views import ListCreateItem, DetailUpdateItem

app_name = 'items'

urlpatterns = [
    path('', ListCreateItem.as_view()),
    # path('<uuid:uuid>', DetailUpdateItem.as_view()),
    path('<uuid:uuid>', DetailUpdateItem.as_view()),
]
