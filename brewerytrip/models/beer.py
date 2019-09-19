from django.db import models
from .brewery import Brewery


class Beer(models.Model):
    id = models.IntegerField(primary_key=True)
    brewery = models.ForeignKey(Brewery, on_delete=models.CASCADE)
    name = models.TextField(blank=True, null=True)
    descript = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'brewerytrip'
        managed = False
        db_table = 'beers'
