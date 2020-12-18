import json
from math import radians, cos, sin, asin, sqrt


def get_distance_from_point(long1, lati1, long2, lati2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [long1, lati1, long2, lati2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def get_coordinates_count(data):
    print(len(data['features']))
    max = 0
    min = 999
    sum = 0
    for geometry in data['features']:
        size = 0
        ltype = geometry['geometry']['type']
        if ltype == "LineString":
            size = len(geometry['geometry']['coordinates'])
        elif ltype == "MultiLineString":
            for line in geometry['geometry']['coordinates']:
                size = size + len(line)
        if size < min:
            min = size
        if size > max:
            max = size
        sum = sum + size
    avg = sum / len(data['features'])
    print("numero de puntos:"+str(sum))
    print("puntos maximos:"+str(max))
    print("puntos minimos:"+str(min))
    print("puntos promedio:"+str(avg))


def get_line_lenght(coordinates):
    size = len(coordinates)
    num = 0
    dist_total = 0
    for point in coordinates:
        nextc = num + 1
        if nextc < size:
            b = coordinates[nextc]
            dist = get_distance_from_point(point[0], point[1], b[0], b[1])
            dist_total = dist_total + dist
            num = num + 1
    return dist_total


def divide_by_type(type, coordinates):
    if type == "LineString":
        return get_line_lenght(coordinates)
    elif type == "MultiLineString":
        size = 0
        for line in coordinates:
            size = size + get_line_lenght(line)
        return size


def get_distances(data):
    max = 0
    min = 999
    sum = 0
    for geometry in data['features']:
        type = geometry['geometry']['type']
        size = divide_by_type(type, geometry['geometry']['coordinates'])
        if size < min:
            min = size
        if size > max:
            max = size
        sum = sum + size

    avg = sum / len(data['features'])
    print("Distancia Total:" + str(sum))
    print("Distancia maxima:" + str(max))
    print("Distancia minima:" + str(min))
    print("Distancia promedio:" + str(avg))


def has_multiline(data):
    for geometry in data['features']:
        type = geometry['geometry']['type']
        if type == "MultiLineString":
            return 1
    return 0


with open('red_primaria.json') as json_file:
    data = json.load(json_file)

get_coordinates_count(data)
print(has_multiline(data))
get_distances(data)


with open('red_vial.geojson', encoding="utf-8") as json_file:
    data = json.load(json_file)

get_coordinates_count(data)
print(has_multiline(data))
get_distances(data)



