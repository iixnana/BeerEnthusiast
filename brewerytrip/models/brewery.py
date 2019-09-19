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

    def filtered_coordinates(self, point, list):
        from brewerytrip.models import Geocode
        from brewerytrip.models import Beer
        coord_list = []
        for var in list:
            beers = Beer.objects.beer_count(var.id)
            if beers > 0:  # remove breweries if they have 0 beers in them
                coord = Geocode.objects.coordinates(var.id)
                dis = distance(point, coord)
                value = beers * (1 - (dis / 1000))
                dir = []  # set direction
                if (coord[0] >= point[0]):  # Latitude
                    dir.append("N")
                else:
                    dir.append("S")
                if (coord[1] >= point[1]):  # Longitude
                    dir.append("E")
                else:
                    dir.append("W")
                coord_list.append((var.id, beers, dis, value, dir, coord))
        return coord_list

class Brewery(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    country = models.TextField(blank=True, null=True)
    objects = BreweryManager()

    class Meta:
        app_label = 'brewerytrip'
        managed = False
        db_table = 'breweries'
