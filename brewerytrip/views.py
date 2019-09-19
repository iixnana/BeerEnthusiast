from django.shortcuts import render
from django.shortcuts import HttpResponse
from . import models


# Create your views here.

def index(request):
    models.print_list((51.355468, 11.100790), 1000)
    breweries = models.Brewery.objects.order_by('name')[:10]
    context = {'breweries': breweries}
    return render(request, 'brewerytrip/index.html', context)


def debug(request, brewery_id):
    geoloc = models.Geocode.objects.coordinates(brewery_id)
    beers = models.Beer.objects.beer_count(brewery_id)
    return HttpResponse("Brewery {} {} {}".format(geoloc[0], geoloc[1], beers))

def results(request):
    latitude = request.POST['latitude']
    longitude = request.POST['longitude']
    context = {'latitude': latitude,
               'longitude': longitude}
    return render(request, 'brewerytrip/results.html', context)
