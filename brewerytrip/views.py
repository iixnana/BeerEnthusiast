from django.shortcuts import render
from django.shortcuts import HttpResponse
from . import models


# Create your views here.

def index(request):
    point = (51.355468, 11.100790)
    return render(request, 'brewerytrip/index.html')


def debug(request, brewery_id):
    geoloc = models.Geocode.objects.coordinates(brewery_id)
    beers = models.Beer.objects.beer_count(brewery_id)
    return HttpResponse("Brewery {} {} {}".format(geoloc[0], geoloc[1], beers))


def results(request):
    latitude = float(request.POST['latitude'])
    longitude = float(request.POST['longitude'])
    route, total_distance, total_beer_types, total_time = models.get_greedy_star((latitude, longitude))
    context = {'latitude': latitude,
               'longitude': longitude,
               'route': route,
               'total_time': total_time,
               'total_distance': total_distance,
               'total_beer_types': total_beer_types}
    return render(request, 'brewerytrip/results.html', context)
