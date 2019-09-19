from django.contrib import admin
from . import models


# Register your models here.
admin.site.register(models.Beer)
admin.site.register(models.Brewery)
admin.site.register(models.Geocode)
