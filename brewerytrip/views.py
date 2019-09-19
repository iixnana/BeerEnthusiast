from django.shortcuts import render
from django.shortcuts import HttpResponse
from . import models
from .models import Brewery


# Create your views here.

def index(request):
    breweries = models.Brewery.objects.order_by('name')[:10]
    context = {'breweries': breweries}
    return render(request, 'brewerytrip/index.html', context)


def debug(request, brewery_id):
    geoloc = models.Brewery.objects.coordinates(brewery_id)
    return HttpResponse("Brewery %s" % geoloc)

def results(request):
    latitude = request.POST['latitude']
    longitude = request.POST['longitude']
    context = {'latitude': latitude,
               'longitude': longitude}
    return render(request, 'brewerytrip/results.html', context)
