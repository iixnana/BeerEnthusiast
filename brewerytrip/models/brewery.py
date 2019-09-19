from django.db import models


class BreweryManager(models.Manager):
    def coordinates(self, id):
        from brewerytrip.models import Geocode
        return Geocode.objects.get(brewery_id__exact=id)


class Brewery(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    objects = BreweryManager()

    def __str__(self):
        return self.id

    class Meta:
        app_label = 'brewerytrip'
        managed = False
        db_table = 'breweries'
