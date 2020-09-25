from django.db import models
import uuid

class RestaurantLocation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256,blank=True, null=True)
    location = models.CharField(max_length=256,blank=True, null=True)
    # category 
    timestamp = models.DateField( auto_now_add = True)
    updated = models.DateField( auto_now = True)

    def __str__(self):
        return self.name