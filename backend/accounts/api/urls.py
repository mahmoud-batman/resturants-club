from django.contrib import admin
from django.urls import path, include
from .views import Users, DetailUpdateUser, CreateUser, DeleteUser, LoginUser

app_name = 'accounts'

urlpatterns = [
    path('', Users.as_view()),
    path('signup/', CreateUser.as_view(), name='create'),
    path('login/', LoginUser.as_view(), name='login'),
    path('<uuid:uuid>/', DetailUpdateUser.as_view()),
    path('<uuid:uuid>/delete/', DeleteUser.as_view()),
]
