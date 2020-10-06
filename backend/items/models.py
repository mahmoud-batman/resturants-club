from django.db import models
from django.contrib.auth import get_user_model
from restaurants.models import RestaurantLocation
from django.db.models.signals import pre_save
from django.dispatch import receiver
import uuid


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    restaurant = models.ForeignKey(
        RestaurantLocation, on_delete=models.CASCADE)

    name = models.CharField(max_length=256)
    contents = models.TextField(help_text='Separate each item by comma')
    excludes = models.TextField(
        blank=True, null=True, help_text='Separate each item by comma')
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-updated', '-timestamp']

#     def get_contents(self):
#         return [x for x in self.contents.split(",")]

#     def get_excludes(self):
#         return [x for x in self.excludes.split(",")]


# @receiver(pre_save, sender=Item)
# def set_contents(sender, **kwargs):
#     instance = kwargs.get("instance")
#     instance.contents = instance.get_contents()

# @receiver(pre_save, sender=Item)
# def set_excludes(sender, **kwargs):
#     instance = kwargs.get("instance")
#     instance.excludes = instance.get_excludes()
