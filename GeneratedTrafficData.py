import csv
from datetime import datetime
import holidays

weather_data_file = 'TrainingData/melbourne_rainfall_data.csv'
temp_data_file = 'TrainingData/melbourne_temp_data.csv'
traffic_data_file = 'TrainingData/traffic_volume_melb_2018_processed.csv'


def read_data_file(file):

    with open(file, 'r', encoding='utf-8-sig') as traffic_volume_file:

        data = []
        reader = csv.reader(traffic_volume_file)

        fieldnames = next(reader)
        csv_reader = csv.DictReader(traffic_volume_file, fieldnames=fieldnames)
        for row in csv_reader:
            dist = {}
            for k, v in row.items():
                dist[k] = v
            data.append(dist)
    return data



def processed_traffic_data_set(dict):

        traffic_data = {}
        traffic_data.update(dict)

        time = dict['TIME']

        Y = time[0:4]
        M = time[4:6]
        D = time[6:8]
        times = Y+'-'+M+'-'+D
        t = datetime.strptime(times, '%Y-%m-%d')

        traffic_data['WEEKDAY'] = t.isoweekday()

        au_holidays = holidays.Australia()

        flag = times in au_holidays

        traffic_data['HOLIDAY'] = flag

        weather_list = read_data_file(weather_data_file)

        for weather_dict in  weather_list:

            Year = weather_dict['Year']
            Month = weather_dict['Month']
            Day = weather_dict['Day']

            weather_times = Year + '-' + Month + '-' + Day

            weather_t = datetime.strptime(weather_times, '%Y-%m-%d')

            if weather_t == t:
                traffic_data['RAINFALL'] = weather_dict['Rainfall amount (millimetres)']

        temp_list = read_data_file(temp_data_file)

        for temp_dict in temp_list:

            Year = temp_dict['Year']
            Month = temp_dict['Month']
            Day = temp_dict['Day']

            temp_times = Year + '-' + Month + '-' + Day

            temp_t = datetime.strptime(temp_times, '%Y-%m-%d')

            if temp_t == t:
                traffic_data['TEMPRETURE'] = temp_dict['Maximum temperature (Degree C)']

     

        with open ('TrainingData/traffic_training_set.csv','a+',newline='') as traffic_training_set:
            w = csv.writer(traffic_training_set)

            w.writerow(traffic_data.values())



if __name__ == "__main__":



    traffic_data_dict = read_data_file(traffic_data_file)

    for dict in traffic_data_dict:

        processed_traffic_data_set(dict)