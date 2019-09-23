from .brewery import Brewery
from .beer import Beer
from .geocode import Geocode
from operator import itemgetter
from haversine import haversine as distance
from copy import deepcopy
import numpy as np
import math
import time

__all__ = ['Brewery', 'Beer', 'Geocode']


def get_greedy_star(home):
    start = time.time()
    route = greedy_star(home)
    end = time.time()
    total_time = end - start
    if route != 0:
        total_distance = 0
        total_beer_types = 0
        route_with_titles = []
        for stop in route:
            total_distance += stop[2]
            total_beer_types += stop[1]
            if stop[0] != 0:
                route_with_titles.append((stop[0], Brewery.objects.find_by_id(stop[0]).name, round(stop[2], 2), stop[1],
                                          Beer.objects.beer_types(stop[0])))
            else:
                route_with_titles.append(('HOME', home, round(stop[2], 2), stop[1]))
        return route_with_titles, total_distance, total_beer_types, total_time
    else:
        return 0, 0, 0, 0


# Main algorithm, where home is coordinates tuple for HOME location
def greedy_star(home):
    total_list = get_list(home, 1000)  # 1000km radius is maximum distance we can reach
    measured_list = list_distance(home, total_list)  # Count distances, directions; general list with coordinates
    layer, dir = layer_and_direction(measured_list)  # Get a sense of which direction and layer is the best target
    if layer == 0:  # Area for searching. From 0 to 450
        set_area = list(sorted(filter(lambda x: x[3] == dir and 0 <= x[2] < 450, measured_list), key=itemgetter(1),
                               reverse=True))
        if (len(set_area) < 50): set_area = list(
            sorted(filter(lambda x: 0 <= x[2] < 700, measured_list), key=itemgetter(1), reverse=True))
    elif layer == 1:  # Area for searching. From 0 to 700
        set_area = list(sorted(filter(lambda x: x[3] == dir and 0 <= x[2] < 700, measured_list), key=itemgetter(1),
                               reverse=True))
        if (len(set_area) < 50): list(
            sorted(filter(lambda x: 0 <= x[2] < 900, measured_list), key=itemgetter(1), reverse=True))
    else:  # Area for searching. From 350 to 1000
        set_area = list(sorted(filter(lambda x: x[3] == dir and 350 <= x[2] <= 1000, measured_list), key=itemgetter(1),
                               reverse=True))
        if (len(set_area) < 50): list(
            sorted(filter(lambda x: 100 <= x[2] <= 1000, measured_list), key=itemgetter(1), reverse=True))
    if (len(set_area) > 0):
        max_beers = 0
        home_var = [0, 0, 0, 'HOME', home]
        max_km = 250
        max_route = []
        for x in range(15, 19):
            # Reset copy of area
            area = deepcopy(set_area)
            km = 2000  # Fuel capacity at 2000km
            point = home  # Starting point
            changed = True
            route = [(home_var[0], home_var[1], 0)]
            collected_beers = 0
            # Check if you are able to travel to the next point and then be able to go home
            while km - distance(point, area[0][4]) - distance(area[0][4], home) >= 0 and changed:
                changed = False
                detour = detour_list(point, area[0][4], area[0][2], area, x)
                queue = make_queue(point, area[0], km - distance(point, area[0][4]) - distance(area[0][4], home),
                                   detour,
                                   max_km)
                total = 0
                for var in queue:
                    km_dist = distance(point, var[4])
                    total += km_dist
                    collected_beers += var[1]
                    area.remove(var)
                    point = var[4]
                    route.append((var[0], var[1], km_dist))
                    changed = True
                km -= total
                area = recount_distances(point, area)
            if km - distance(point, home) >= 0:
                total = 0
                home_var[2] = distance(point, home)
                detour = detour_list(point, home, home_var[2], area, x)
                queue = make_queue(point, home_var, km - home_var[2], detour, km - home_var[2])
                for var in queue:
                    km_dist = distance(point, var[4])
                    total += km_dist
                    collected_beers += var[1]
                    point = var[4]
                    route.append((var[0], var[1], km_dist))
                km -= total
                if max_beers < collected_beers:
                    max_beers = collected_beers
                    max_route.clear()
                    max_route = route
                    print(">>>")
                # print("Finished with %dkm left. Collected %s. %s degree" % (km, collected_beers, x))
            else:
                print("Error :(")
        return max_route
    else:
        return 0


# Find best detour points. List is sorted by beer types count in the brewery, so breweries with most value get priority
def make_queue(start, end, km, detour, max_km):
    if km > max_km: km = max_km
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


# Recount distances to other breweries in the area
def recount_distances(point, area):
    for var in area:
        var[2] = distance(point, var[4])
    return area


# Count value of layers and directions
def layer_and_direction(filtered_list):
    group = [0, 0, 0]
    directions = [['NE', 0], ['SE', 0], ['NW', 0], ['SW', 0]]
    for var in filtered_list:
        if 0 <= var[2] < 350:
            if var[3] == 'NE':
                directions[0][1] += var[1]
            elif var[3] == 'SE':
                directions[1][1] += var[1]
            elif var[3] == 'NW':
                directions[2][1] += var[1]
            else:
                directions[3][1] += var[1]
            group[0] += var[1]
        elif 350 <= var[2] < 700:
            if var[3] == 'NE':
                directions[0][1] += var[1]
            elif var[3] == 'SE':
                directions[1][1] += var[1]
            elif var[3] == 'NW':
                directions[2][1] += var[1]
            else:
                directions[3][1] += var[1]
            group[1] += var[1]
        else:
            if var[3] == 'NE':
                directions[0][1] += var[1]
            elif var[3] == 'SE':
                directions[1][1] += var[1]
            elif var[3] == 'NW':
                directions[2][1] += var[1]
            else:
                directions[3][1] += 1
            group[2] += var[1]
    if group[0] >= group[1] and group[0] >= group[2]:
        layer = 0
    elif group[1] >= group[0] and group[1] >= group[2]:
        layer = 1
    else:
        layer = 2
    if directions[0] >= directions[1] and directions[0] >= directions[2] and directions[0] >= directions[3]:
        direction = 'NE'
    elif directions[1] >= directions[0] and directions[1] >= directions[2] and directions[1] >= directions[3]:
        direction = 'SE'
    elif directions[2] >= directions[1] and directions[2] >= directions[0] and directions[2] >= directions[3]:
        direction = 'NW'
    else:
        direction = 'SW'
    return layer, direction


# Filter area to breweries on 10 degrees, up to
def detour_list(start, end, dist, area, degrees):
    return list(filter(lambda x: x[2] < dist and edge(start, end, x[4]) <= degrees, area))


# Count edge of a triangle
def edge(start, end, mid):
    c = distance(start, end)
    b = distance(start, mid)
    a = distance(mid, end)
    if b > 0 and c > 0:
        degree = math.degrees(np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)))
        return degree
    else:
        return 0


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
    return Brewery.objects.filtered_coordinates(point, filtered)


# Filter breweries in set distance, for example in radius of 1000km
def get_list(point, dis):
    return Brewery.objects.filter_breweries(point, dis)


# Set reference direction: North, South, West, East
def direction(reference_point, point):
    if point[0] >= reference_point[0] and point[1] >= reference_point[1]:  # Latitude
        return 'NE'
    elif point[0] <= reference_point[0] and point[1] >= reference_point[1]:
        return 'SE'
    elif point[0] >= reference_point[0] and point[1] <= reference_point[1]:  # Longitude
        return 'NW'
    else:
        return 'SW'
