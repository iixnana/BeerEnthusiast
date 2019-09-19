from django.db import models
from .brewery import Brewery


class GeocodeManager(models.Manager):
    def coordinates(self, id):
        point = self.get(brewery_id__exact=id)
        return (point.latitude, point.longitude)

class Geocode(models.Model):
    id = models.IntegerField(primary_key=True)
    brewery = models.ForeignKey(Brewery, on_delete=models.CASCADE)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    objects = GeocodeManager()

    class Meta:
        app_label = 'brewerytrip'
        managed = False
        db_table = 'geocodes'
