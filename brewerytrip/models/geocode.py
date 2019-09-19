from django.db import models
from .brewery import Brewery


class Geocode(models.Model):
    id = models.IntegerField(primary_key=True)
    brewery = models.ForeignKey(Brewery, on_delete=models.CASCADE)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return 'NO {} , where Latitude: {} Longitude: {}'.format(self.brewery_id, self.latitude, self.longitude)

    class Meta:
        app_label = 'brewerytrip'
        managed = False
        db_table = 'geocodes'
