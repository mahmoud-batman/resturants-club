from django.db import models
import uuid
from core.utils.unique_slug import unique_slug_generator
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class RestaurantLocation(models.Model):

    class CATEGORY_CHOICES(models.TextChoices):
        RESTAURANT = 'RS', _('Restaurant')
        CAFE = 'CF', _('Cafe')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256, blank=True, null=True)
    location = models.CharField(max_length=256, blank=True, null=True)
    category = models.CharField(
        max_length=2, choices=CATEGORY_CHOICES.choices, default=CATEGORY_CHOICES.RESTAURANT)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def title(self):
        """ we added title property to be used in unique_slug_generator method """
        return self.name


@receiver(pre_save, sender=RestaurantLocation)
def add_slug(sender, **kwargs):
    instance = kwargs.get("instance")
    name = instance.name
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
