from django.shortcuts import render
from django.shortcuts import HttpResponse
from . import models


# Create your views here.

def index(request):
    point = (51.355468, 11.100790)
    breweries = models.greedy_star(point)
    # breweries = models.Brewery.objects.order_by('name')[:10]
    context = {'list': breweries,
               'first_stop': point}
    return render(request, 'brewerytrip/index.html', context)


def debug(request, brewery_id):
    geoloc = models.Geocode.objects.coordinates(brewery_id)
    beers = models.Beer.objects.beer_count(brewery_id)
    return HttpResponse("Brewery {} {} {}".format(geoloc[0], geoloc[1], beers))


def results(request):
    latitude = float(request.POST['latitude'])
    longitude = float(request.POST['longitude'])
    result = models.greedy_star((latitude, longitude))
    context = {'latitude': latitude,
               'longitude': longitude,
               'result': result}
    return render(request, 'brewerytrip/results.html', context)
