import csv
import time

import couchdb
from suds.client import Client
import urllib
import requests
import json
import pandas as pd


url = 'http://sciwebsvc.epa.vic.gov.au/aqapi/sites'

host = 'http://sciwebsvc.epa.vic.gov.au/aqapi/Measurements?'
site = 'siteId='
monitor='&monitorId=BPM2.5'
time_basis= '&timebasisid=1HR_AV'
time_period = '&fromDate=2018010100&toDate=2018123123'

count_flag = 0


def register_sites_url():
    try:
        response = requests.get(url)
        data = response.json()

        json_str = json.dumps(data)
        return json_str

    except Exception as e:
        pass


def get_EPA_sites_info(sites_info):
    sites_EPA = []

    for key, value in sites_info.items():

        if key == 'Sites':
            sites_EPA = value

    return sites_EPA


def get_EPA_sites_ID(sites):

    sites_id = []

    for dict in sites:

        for key,value in dict.items():

            if key == 'SiteId':

                sites_id.append(value)

    return sites_id


def register_EPA_sites(id):

    try:

        EPA_url = host + site + str(id) + monitor +time_basis + time_period
        response = requests.get(EPA_url)
        data = response.json()

        json_str = json.dumps(data)

        data = json.loads(json_str)

        return data

    except Exception as e:
        print("Exceptions on get EPA data")


def get_EPA_measurements(data):

    measurements= []

    for key,value in data.items():

        if key == 'Measurements':

            measurements = value

    return measurements


"""
def store_EPA_data(data):

    try:

        for dict in data:
            Station = dict.get('SiteId')
            Time_Raw = dict.get('DateTimeStart')
            Time = Time_Raw.replace('T', '').replace(':00:00', '').replace('-', '')
            Longitude = dict.get('Longitude')
            Latitude = dict.get('Latitude')
            Value = dict.get('Value')

            doc = {

                'Station': Station,
                'Time': Time,
                'Longitude': Longitude,
                'Latitude': Latitude,
                'Value': Value,
            }
            
            store_in_database(doc)

            print(doc)

    except Exception as e:

        print("Couldn;t genarated epa data in to doc")
"""


def store_EPA_data(data):


    for dict in data:

        Station = dict.get('SiteId')
        Time_Raw = dict.get('DateTimeStart')
        Time = Time_Raw.replace('T', '').replace(':00:00', '').replace('-', '')
        Longitude = dict.get('Longitude')
        Latitude = dict.get('Latitude')
        Value = dict.get('Value')

        doc = {

            'Station': Station,
            'Time': Time,
            'Longitude': Longitude,
            'Latitude': Latitude,
            'Value': Value,
        }

        file ='epa_pollution_data.csv'

        store_in_csv(doc,file)
        #store_in_database(doc)

        print(type(doc))

def store_in_csv(dict,file):

    with open(file,'a+') as f:
        w = csv.writer(f)

        #w.writerow(dict.keys())


        w.writerow(dict.values())




def store_in_database(doc):

    try:
        server = couchdb.Server('http://127.0.0.1:5984')

        database = server['epa_pollution_data']

        database.save(doc)


    except Exception as e:

        print("Couldn't store data"+ doc +"into database")


if __name__ == "__main__":

    data = register_sites_url()

    EPA_sites = {}

    EPA_sites = json.loads(data)

    sites = get_EPA_sites_info(EPA_sites)

    sites_id = get_EPA_sites_ID(sites)

    for id in sites_id:
        EPA_data_raw = {}

        EPA_data_raw = register_EPA_sites(id)

        EPA_data = get_EPA_measurements(EPA_data_raw)

        store_EPA_data(EPA_data)

        print(str(id) + "    finished")

    print("Program finished")
