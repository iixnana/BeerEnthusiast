from .brewery import Brewery
from .beer import Beer
from .geocode import Geocode
from operator import itemgetter
from haversine import haversine as distance
__all__ = ['Brewery', 'Beer', 'Geocode']


def pick(dir, list, point):
    print(dir)
    list = filter(lambda x: x[4] == dir, list)
    group = [0, 0, 0]
    group0 = []
    group1 = []
    group2 = []
    for var in list:
        if 0 <= var[2] < 350:
            group[0] += var[3]
            group0.append(var)
        elif 350 <= var[2] < 700:
            group[1] += var[3]
            group1.append(var)
        else:
            group[2] += var[3]
            group2.append(var)
    print("Group 0 %s" % group[0])
    print("Group 1 %s" % group[1])
    print("Group 2 %s" % group[2])
    group1 = sorted(group1, key=itemgetter(3), reverse=True)
    km = 2000
    collected_beers = 0
    home = point
    while (km - distance(group1[0][5], point) >= distance(group1[0][5], home)):
        km -= distance(group1[0][5], point)
        point = group1[0][5]
        collected_beers += group1[0][1]
        group1.pop(0)
    km -= distance(group1[0][5], home)  # go home
    print("End %s %s" % (km, collected_beers))
    return km


def weigh_directions(list):
    list = sorted(list, key=itemgetter(4))
    directions = [['SE', 0], ['SW', 0], ['NE', 0], ['NW', 0]]
    for var in list:
        if var[4] == 'NE':
            directions[2][1] += var[3]
        elif var[4] == 'NW':
            directions[3][1] += var[3]
        elif var[4] == 'SE':
            directions[0][1] += var[3]
        else:
            directions[1][1] += var[3]
    return max(directions)[0]


def measure_distance(point, filtered):
    list = Brewery.objects.filtered_coordinates(point, filtered)
    list = sorted(list, key=itemgetter(1), reverse=True)  # put priority on breweries, which have lots of beer kinds
    return list


def list(point, dis):
    list = Brewery.objects.filter_breweries(point, dis)
    print(len(list))
    return list


def direction(reference_point, point):
    if (point[0] >= reference_point[0] and point[1] >= reference_point[1]):  # Latitude
        return 'NE'
    elif (point[0] <= reference_point[0] and point[1] >= reference_point[1]):
        return 'SE'
    elif (point[0] >= reference_point[0] and point[1] <= reference_point[1]):  # Longitude
        return 'NW'
    else:
        return 'SW'
