from .brewery import Brewery
from .beer import Beer
from .geocode import Geocode
from operator import itemgetter
from haversine import haversine as distance
import numpy as np
import math

__all__ = ['Brewery', 'Beer', 'Geocode']


def greedy_star(home):
    total_list = get_list(home, 1000)  # 1000km radius is maximum distance we can reach
    measured_list = list_distance(home, total_list)  # Count distances, directions; general list with coordinates
    layer, dir = layer_and_direction(measured_list)
    if layer == 0:
        area = sorted(filter(lambda x: x[3] == dir and 0 <= x[2] < 350, measured_list), key=itemgetter(1), reverse=True)
    elif layer == 1:
        area = sorted(filter(lambda x: x[3] == dir and 0 <= x[2] < 700, measured_list), key=itemgetter(1), reverse=True)
    else:
        area = sorted(filter(lambda x: x[3] == dir and 350 <= x[2] <= 1000, measured_list), key=itemgetter(1),
                      reverse=True)
    km = 2000
    collected_beers = 0
    point = home
    changed = True
    while km - distance(point, area[0][4]) - distance(area[0][4], home) >= 0 and changed:
        changed = False
        detour = detour_list(point, area[0][4], area[0][2], area)
        queue = make_queue(point, area[0], km - distance(point, area[0][4]) - distance(area[0][4], home), detour)
        total = 0
        for var in queue:
            total += distance(point, var[4])
            collected_beers += var[1]
            area.remove(var)
            point = var[4]
            changed = True
        km -= total
        print(km)
        print(collected_beers)
        area = recount_distances(point, area)
    if km - distance(point, home) >= 0:
        total = 0
        detour = detour_list(point, home, distance(point, home), area)
        home = [0, 0, distance(point, home), '', home]
        queue = make_queue(point, home, km, detour)
        for var in queue:
            total += distance(point, var[4])
            collected_beers += var[1]
            point = var[4]
        km -= total
        print("Finished with %s. Collected %s" % (km, collected_beers))
    else:
        km -= distance(point, home)

    return queue


"""
    detour = detour_list(home, area[0][4], area[0][2], area)
    queue = make_queue(home, area[0], 300, detour)
    total = 0
    for var in queue:
        total += distance(point, var[4])
        collected_beers += var[1]
        area.remove(var)
        point = var[4]

    print(total)
    print(collected_beers)

    area = recount_distances(point, area)

    detour = detour_list(point, area[0][4], area[0][2], area)
    queue = make_queue(point, area[0], 300, detour)
    for var in queue:
        total += distance(point, var[4])
        collected_beers += var[1]
        area.remove(var)
        point = var[4]
    print(total)
    print(collected_beers)

    area = recount_distances(point, area)

    detour = detour_list(point, area[0][4], area[0][2], area)
    queue = make_queue(point, area[0], 300, detour)
    for var in queue:
        total += distance(point, var[4])
        collected_beers += var[1]
        area.remove(var)
        point = var[4]
    print(total)
    print(collected_beers)
"""


def make_queue(start, end, km, detour):
    if (km > 250): km = 250
    queue = [end]
    while km > 0 and len(detour) > 0:
        total_distance = 0
        queue.insert(0, detour[0])
        detour.pop(0)
        point = start
        for var in queue:
            total_distance += distance(point, var[4])
            point = var[4]
        if km < total_distance - end[2]: queue.pop(0)
    return queue


def recount_distances(point, area):
    for var in area:
        var[2] = distance(point, var[4])
    return area


"""
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
    group0 = sorted(group0, key=itemgetter(3), reverse=True)
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
"""

# Count value of layers and directions
def layer_and_direction(list):
    group = [0, 0, 0]
    directions = [['NE', 0], ['SE', 0], ['NW', 0], ['SW', 0]]
    for var in list:
        if 0 <= var[2] < 350:
            if (var[3] == 'NE'):
                directions[0][1] += var[1]
            elif (var[3] == 'SE'):
                directions[1][1] += var[1]
            elif (var[3] == 'NW'):
                directions[2][1] += var[1]
            else:
                directions[3][1] += var[1]
            group[0] += var[1]
        elif 350 <= var[2] < 700:
            if (var[3] == 'NE'):
                directions[0][1] += var[1]
            elif (var[3] == 'SE'):
                directions[1][1] += var[1]
            elif (var[3] == 'NW'):
                directions[2][1] += var[1]
            else:
                directions[3][1] += var[1]
            group[1] += var[1]
        else:
            if (var[3] == 'NE'):
                directions[0][1] += var[1]
            elif (var[3] == 'SE'):
                directions[1][1] += var[1]
            elif (var[3] == 'NW'):
                directions[2][1] += var[1]
            else:
                directions[3][1] += 1
            group[2] += var[1]
    if (group[0] >= group[1] and group[0] >= group[2]):
        layer = 0
    elif (group[1] >= group[0] and group[1] >= group[2]):
        layer = 1
    else:
        layer = 2
    if (directions[0] >= directions[1] and directions[0] >= directions[2] and directions[0] >= directions[3]):
        dir = 'NE'
    elif (directions[1] >= directions[0] and directions[1] >= directions[2] and directions[1] >= directions[3]):
        dir = 'SE'
    elif (directions[2] >= directions[1] and directions[2] >= directions[0] and directions[2] >= directions[3]):
        dir = 'NW'
    else:
        dir = 'SW'
    return layer, dir


def detour_list(start, end, distance, area):
    return list(filter(lambda x: x[2] < distance and edge(start, end, x[4]) <= 5, area))


# Count edge of a triangle
def edge(start, end, mid):
    c = distance(start, end)
    b = distance(start, mid)
    a = distance(mid, end)
    degree = math.degrees(np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)))
    return degree


# Find out value by 4 directions
def weigh_directions(list):
    list = sorted(list, key=itemgetter(3))
    directions = [['SE', 0], ['SW', 0], ['NE', 0], ['NW', 0]]
    for var in list:
        if var[3] == 'NE':
            directions[2][1] += var[3]
        elif var[3] == 'NW':
            directions[3][1] += var[3]
        elif var[3] == 'SE':
            directions[0][1] += var[3]
        else:
            directions[1][1] += var[3]
    return max(directions)[0]


# Measure distances to all breweries from a reference point
def list_distance(point, filtered):
    list = Brewery.objects.filtered_coordinates(point, filtered)
    return list


# Filter breweries in set distance, for example in radius of 1000km
def get_list(point, dis):
    list = Brewery.objects.filter_breweries(point, dis)
    return list


# Set reference direction: North, South, West, East
def direction(reference_point, point):
    if (point[0] >= reference_point[0] and point[1] >= reference_point[1]):  # Latitude
        return 'NE'
    elif (point[0] <= reference_point[0] and point[1] >= reference_point[1]):
        return 'SE'
    elif (point[0] >= reference_point[0] and point[1] <= reference_point[1]):  # Longitude
        return 'NW'
    else:
        return 'SW'
