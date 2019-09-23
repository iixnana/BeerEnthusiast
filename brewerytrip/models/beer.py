from django.db import models
from .brewery import Brewery


class BeerManager(models.Manager):
    def beer_count(self, id):
        return self.filter(brewery_id__exact=id).count()

    def beer_types(self, id):
        return list(self.filter(brewery_id__exact=id))


class Beer(models.Model):
    id = models.IntegerField(primary_key=True)
    brewery = models.ForeignKey(Brewery, on_delete=models.CASCADE)
    name = models.TextField(blank=True, null=True)
    descript = models.TextField(blank=True, null=True)
    objects = BeerManager()

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'brewerytrip'
        managed = False
        db_table = 'beers'
