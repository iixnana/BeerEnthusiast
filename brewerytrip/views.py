from django.shortcuts import render
from django.http import HttpResponse
from .models import Beer, Brewery, Geocode


# Create your views here.


def index(request):
    breweries = Brewery.objects.order_by('name')[:10]
    context = {'breweries': breweries}
    return render(request, 'brewerytrip/index.html', context)


def results(request):
    latitude = request.POST['latitude']
    longitude = request.POST['longitude']
    context = {'latitude': latitude,
               'longitude': longitude}
    return render(request, 'brewerytrip/results.html', context)
