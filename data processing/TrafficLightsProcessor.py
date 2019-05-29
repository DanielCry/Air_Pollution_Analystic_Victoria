import csv
from shapely.geometry import Polygon
from shapely.geometry import Point
import couchdb


with open('Data/traffic_lights.csv', 'r', encoding='utf-8-sig') as traffic_lights_file:

    traffic_lights = []

    reader = csv.reader(traffic_lights_file)

    fieldnames = next(reader)
    csv_reader = csv.DictReader(traffic_lights_file, fieldnames=fieldnames)
    for row in csv_reader:
        dist = {}
        for k, v in row.items():
            dist[k] = v

        traffic_lights.append(dist)


coords = [(-37.812412,144.953805), (-37.820420,144.957598), (-37.815278, 144.974972), (-37.807527, 144.971216)]

MelbourneCBD = Polygon(coords)
melbourne_traffic_lights = []

for location_dict in traffic_lights:

    location_point = Point(float(location_dict['Y']), float(location_dict['X']))

    if location_point.within(MelbourneCBD):

        melbourne_traffic_lights.append(location_dict)

#couch = couchdb.Server('http://127.0.0.1:5984/')

#traffic_lights_melbourne_database = couch.create('traffic_lights_melbourne')
#traffic_lights_database = couch.create('traffic_lights')


def store_in_csv(dict, file):
    with open(file, 'a+') as f:
        w = csv.writer(f)

        # w.writerow(dict.keys())

        w.writerow(dict.values())

for location in melbourne_traffic_lights:
    #traffic_lights_melbourne_database.save(location)
    store_in_csv(location,'melbourne_traffic_lights.csv')



for location in traffic_lights:
    #traffic_lights_database.save(location)
    store_in_csv(location, 'victoria_traffic_lights.csv')
