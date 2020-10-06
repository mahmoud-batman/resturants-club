
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/items/', include('items.api.urls', namespace='items')),
    path('api/v1/accounts/', include('accounts.api.urls', namespace='accounts')),
    path('api/v1/restaurants/',
         include('restaurants.api.urls', namespace='restaurants'))
]
