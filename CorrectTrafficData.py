import csv
traffic_data_file = 'TrainingData/traffic_training_set.csv'

melbbourne_traffic_file = 'melbourne_traffic_lights.csv'


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


def correct_traffic_data(dict):

    traffic_data = {}
    traffic_data.update(dict)

    melbourne_list = read_data_file(melbbourne_traffic_file)

    for lights in melbourne_list:

        if traffic_data['SITE_NO'] == lights['SITE_NO']:

            traffic_data['X'] = lights['X']
            traffic_data['Y'] = lights['Y']

    with open('TrainingData/traffic_training_set_correct.csv', 'a+', newline='') as traffic_training_set:

        w = csv.writer(traffic_training_set)

        w.writerow(traffic_data.values())






if __name__ == "__main__":



    traffic_data_dict = read_data_file(traffic_data_file)

    for dict in traffic_data_dict:

        correct_traffic_data(dict)