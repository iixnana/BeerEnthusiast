from django.db import models
from haversine import haversine as distance



class BreweryManager(models.Manager):
    def filter_breweries(self, point, km):
        from brewerytrip.models import Geocode
        filtered = []
        for brewery in self.all():
            if km > distance(point, Geocode.objects.coordinates(brewery.id)):
                filtered.append(brewery)
        return filtered

class Brewery(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    objects = BreweryManager()

    class Meta:
        app_label = 'brewerytrip'
        managed = False
        db_table = 'breweries'
