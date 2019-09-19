from .brewery import Brewery
from .beer import Beer
from .geocode import Geocode
from haversine import haversine as distance


__all__ = ['Brewery', 'Beer', 'Geocode']


def hello():
    print("This is a function")


def print_list(point, dis):
    list = Brewery.objects.filter_breweries(point, dis)
    for val in list:
        print(val.name)
    print(len(list))
