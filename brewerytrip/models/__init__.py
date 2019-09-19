from .brewery import Brewery
from .beer import Beer
from .geocode import Geocode
from operator import itemgetter
from haversine import haversine as distance
__all__ = ['Brewery', 'Beer', 'Geocode']


def pick_brewery()


def weigh_directions(list):
    list = sorted(list, key=itemgetter(4), reverse=True)
    directions = [["SE", 0, 0], ["SW", 0, 0], ["NE", 0, 0], ["NW", 0, 0]]
    for var in list:
        if var[4][0] == 'N' and var[4][1] == 'E':
            directions[2][1] += var[3]
            # directions[2][2] += var[1]
        elif var[4][0] == 'N' and var[4][1] == 'W':
            directions[3][1] += var[3]
            # directions[3][2] += var[1]
        elif var[4][0] == 'S' and var[4][1] == 'E':
            directions[0][1] += var[3]
            # directions[0][2] += var[1]
        else:
            directions[1][1] += var[3]
            # directions[1][2] += var[1]
    for dir in directions:
        print(dir)


def measure_distance(point, filtered):
    list = Brewery.objects.filtered_coordinates(point, filtered)
    list = sorted(list, key=itemgetter(1), reverse=True)  # put priority on breweries, which have lots of beer kinds
    for var in list:
        print(var)
    return list


def list(point, dis):
    list = Brewery.objects.filter_breweries(point, dis)
    print(len(list))
    return list


def direction(reference_point, point):
    dir = []
    if (point[0] > reference_point[0]):  # Latitude
        dir.append("N")
    else:
        dir.append("S")
    if (point[1] > reference_point[1]):  # Longitude
        dir.append("E")
    else:
        dir.append("W")
    return dir
