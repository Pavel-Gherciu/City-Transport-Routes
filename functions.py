import database
import random
from collections import defaultdict, deque
from typing import List, Tuple


def numBusesToDestination(routes: List[List[int]], source: int, target: int, stops_map: dict = None) -> Tuple[
    int, List[Tuple[int, int]]]:
    # Base case
    if source == target:
        return 0, [(0, source)]
    # Creating graph or routes
    graph = defaultdict(set)

    # If stops_map is provided, replace the stops in routes with their equivalent stops
    if stops_map:
        for i in range(len(routes)):
            for j in range(len(routes[i])):
                routes[i][j] = stops_map.get(routes[i][j], routes[i][j])

    # Since index represents bus_number on a route
    # suppose i is bus number and stops are the values present at that index
    for bus_number, stops in enumerate(routes):
        # for each stop adding buses going to that stop
        for stop in stops:
            graph[stop].add(bus_number)

    # Using bfs
    bfs = deque([(source, 0, [(0, source)])])

    # visited stops
    seen_stops = set()
    # visited buses
    seen_buses = set()

    while bfs:
        stop, count, route = bfs.popleft()
        # Resulting case
        if stop == target:
            return count, route

        # Since our graph stores all buses going to a stop
        # We will iterate for every bus
        for bus_number in graph[stop]:
            # We dont want to travel in same bus as we might stuck into loop and reach nowhere
            if bus_number not in seen_buses:
                seen_buses.add(bus_number)

                # Now we are in a bus, so we will travel all the stops that bus goes to but again, we only want to go to stops we haven't visited
                for next_stop in routes[bus_number]:
                    if next_stop not in seen_stops:
                        seen_stops.add(next_stop)
                        bfs.append((next_stop, count + 1, route + [(bus_number, next_stop)]))
    return -1, []


def get_stops(start, end, num_list):
    stops = []
    if start <= end:  # count forwards
        for i in num_list:
            if start <= i <= end:
                stops.append(i)
                if i == end:
                    break
    else:  # count backwards
        for i in reversed(num_list):
            if end <= i <= start:
                stops.append(i)
                if i == end:
                    break
    return stops


def travel_time(lst):
    distance = len(lst) - 1

    total_time = 0
    for i in range(distance):
        travel_time = random.randint(1, 2)
        total_time += travel_time
    total_time += distance

    return total_time


def get_coords(stoplist):
    return [database.stops_coord[f"s{index}"] for index in stoplist]

def get_specific_coord(stoplist, index):
    stop_key = f"s{index}"
    return stoplist[stop_key]

def randomcolor():
    hex_chars = '0123456789ABCDEF'
    color_code = '#' + ''.join(random.choice(hex_chars) for _ in range(6))
    return color_code

def bus_check(bus_number):
    match bus_number:
        case 0:
            return 12
        case 1:
            return 22
        case 2:
            return 13
        case 3:
            return 13
        case 4:
            return 10
        case 5:
            return 7


stops_key_list = list(database.stops.keys())
stops_value_list = list(database.stops.values())

local_routes = database.routes

routes = [[1, 2, 7], [3, 6, 7], [4, 6, 5]]


"""
source = 1
target = 34
num_buses, route = numBusesToDestination(database.routes, source, target, database.stops_map)


if num_buses == -1:
    print("It is not possible to reach the destination")
else:
    print("Minimum number of buses required:", num_buses)
    print("Route taken:")
    for i, (bus_number, stop) in enumerate(route):
        if i == 0:
            print(f"Start at stop {stops_value_list[stop-1]}")
        elif i == len(route) - 1:
            print(f"Take bus {bus_number} to stop {stops_value_list[stop-1]}")
            print(f"Arrive at stop {stops_value_list[stop-1]}")
        else:
            print(f"Take bus {bus_number} to stop {stops_value_list[stop-1]}")


print("Statiile parcurse:")
time = 0
for i in range(len(route) - 1):
    a, b = route[i]
    c, d = route[i+1]
    stops_list = get_stops(b, d, database.routes[c])
    print(stops_list)
    time += travel_time(stops_list)
print("This is the total time passed:")
print(time)
"""
