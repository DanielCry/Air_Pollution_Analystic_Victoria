from math import sin,asin,cos,radians,fabs,sqrt
import csv

EARTH_RADIUS = 6371

epa_station = [

{'SITE_NO': '10003', 'X':'-37.80488', 'Y':'144.8728'},
{'SITE_NO': '10217', 'X':'-38.23929', 'Y':'146.3873'},
{'SITE_NO': '10239', 'X':'-37.8074', 'Y':'144.97'},
{'SITE_NO': '10218', 'X':'-38.18647', 'Y':'146.2583'},
{'SITE_NO': '10107', 'X':'-38.17356', 'Y':'144.3703'},
{'SITE_NO': '10219', 'X':'-38.30431', 'Y':'146.4149'},
{'SITE_NO': '10001', 'X':'-37.77841', 'Y':'145.0306'},
{'SITE_NO': '10017', 'X':'-38.22939', 'Y':'146.4245'},
{'SITE_NO': '10011', 'X':'-38.19428', 'Y':'146.5315'}

               ]

def hav(theta):
    s = sin(theta / 2)
    return s * s

def get_distance_hav(lat0, lng0, lat1, lng1):
    "用haversine公式计算球面两点间的距离。"
    # 经纬度转换成弧度
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lng0)
    lng1 = radians(lng1)

    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))

    return distance


def get_vic_road_site():

    with open('victoria_traffic_lights.csv','r',encoding='utf-8-sig') as traffic_lights_victoria:

        reader = csv.reader(traffic_lights_victoria)
        traffic_volume_victoria =[]
        traffic_sites_victoria =[]

        fieldnames = next(reader)
        csv_reader = csv.DictReader(traffic_lights_victoria, fieldnames = fieldnames)

        for row in csv_reader:

            dict = {}

            for k,v in row.items():
                dict[k]=v
            traffic_volume_victoria.append(dict)

    for victoria_dict in traffic_volume_victoria:
        #print(victoria_dict)

        for k,v in victoria_dict.items():
            traffic_sites_victoria_dict = {}

            if k == 'SITE_NO':

                traffic_sites_victoria_dict['SITE_NO'] = victoria_dict['SITE_NO']
                traffic_sites_victoria_dict['X'] = victoria_dict['X']
                traffic_sites_victoria_dict['Y'] = victoria_dict['Y']

            #print(traffic_sites_victoria)

            if traffic_sites_victoria_dict:

                traffic_sites_victoria.append(traffic_sites_victoria_dict)

    return traffic_sites_victoria


if __name__=="__main__":

    traffic_volume = get_vic_road_site()
    traffic_volume_victoria = []

    distance_flag = 9999999999999

    result = []

    for dict in epa_station:

        station_site ={}

        x1 = float(dict['X'])
        y1 = float(dict['Y'])

        for traffic_dict in traffic_volume:

           # print(traffic_dict)

            if 'X' in traffic_dict:
                x2 = float(traffic_dict['X'])
            if 'Y' in traffic_dict:
                y2 = float(traffic_dict['Y'])

            distance = get_distance_hav(x1, y1, x2, y2)

            if distance < distance_flag:



                station_site ['SITE_NO'] = traffic_dict['SITE_NO']
                station_site ['STATION'] = dict['SITE_NO']
                station_site['DISTANCE'] = distance

                distance_flag = distance

        traffic_volume_victoria.append(station_site)

        distance_flag = 9999999999999
    print(traffic_volume_victoria)