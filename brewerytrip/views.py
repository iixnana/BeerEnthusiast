from django.shortcuts import render
from django.shortcuts import HttpResponse
from . import models


# Create your views here.

def index(request):
    point = (51.355468, 11.100790)
    list = models.list(point, 1000)  # filter to breweries in 1000km circle - it's impossible to go more far
    measure = models.measure_distance(point, list)
    models.weigh_directions(measure)
    pick = models.pick(models.weigh_directions(measure), measure, point)
    # breweries = models.Brewery.objects.order_by('name')[:10]
    context = {'list': measure,
               'first_stop': pick}
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
