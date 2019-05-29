import csv


first_file_path = 'Data/VicRoadData/VSDATA_2018'


def parsing_traffic_volumes(filename):

    with open(filename, 'r', encoding='utf-8-sig') as volume_data:
        reader = csv.reader(volume_data)

        traffic_volums = []
        fieldnames = next(reader)
        csv_reader = csv.DictReader(volume_data, fieldnames=fieldnames)
        for row in csv_reader:
            dist = {}
            for k, v in row.items():
                dist[k] = v

            traffic_volums.append(dist)


def generate_file_name(month,day):

    day_index = 1
    file_path = []
    if month < 10:
        second_file_path = first_file_path + '0' + str(month)
    else:
        second_file_path = first_file_path + str(month)

    for day_index in range(1, day, 1):

        if month < 10:

            if day_index < 10:

                third_file_path = second_file_path + '/VSDATA_2018' + '0' + str(month) + '0' + str(
                    day_index) + '.csv'

                file_path.append(third_file_path)

            else:
                third_file_path = second_file_path + '/VSDATA_2018' + '0' + str(month) + str(day_index) + '.csv'
                file_path.append(third_file_path)


        else:


            if day_index < 10:

                third_file_path = second_file_path + '/VSDATA_2018' + str(month_index) + '0' + str(day_index) + '.csv'
                file_path.append(third_file_path)

            else:
                third_file_path = second_file_path + '/VSDATA_2018' + str(month_index) + str(day_index) + '.csv'

                file_path.append(third_file_path)

    return file_path


def parsing_traffic_volume(file):

    with open(file, 'r', encoding='utf-8-sig') as traffic_volume_file:

        traffic_volume = []

        reader = csv.reader(traffic_volume_file)

        fieldnames = next(reader)
        csv_reader = csv.DictReader(traffic_volume_file, fieldnames=fieldnames)

        #在这里进行行处理
        #先删除不需要的值，在横着合并同一个字典内的数据，在合并不同字典内的数据，最后创建csv文件并些把data写入

        for row in csv_reader:
            dist = {}
            for k, v in row.items():

                dist[k] = v
            traffic_volume.append(dist)

    for vic_road_dict in  traffic_volume:

        useless = ('NM_REGION', 'CT_RECORDS', 'QT_VOLUME_24HOUR','CT_ALARM_24HOUR','NB_DETECTOR')

        for delete_key in useless:
            if delete_key in vic_road_dict:
                del vic_road_dict[delete_key]

        processed_data = genarated_new_data_file(vic_road_dict)

        with open('processed_HX_data.csv', 'a+') as vic_data:

            w = csv.writer(vic_data)

            w.writerow(processed_data.values())


    print(traffic_volume)
    print('\n')


def genarated_new_data_file(vic_road_dict):

    #横向加合车流量数据

    traffic_volume_data = {}
    volume_value = 0

    if 'NB_SCATS_SITE' in vic_road_dict:
        traffic_volume_data['SITE'] =  vic_road_dict['NB_SCATS_SITE']

    if 'QT_INTERVAL_COUNT' in vic_road_dict:

        #转好日期格式
        date_raw = vic_road_dict['QT_INTERVAL_COUNT']


    for index in range(0, 96):

        if index % 4 == 0:

            traffic_volume_data[str.format("%02d",index % 4)] = volume_value

            volume_value = 0

        volume_key = "V" + str.format("%02d", index)

        if volume_key in vic_road_dict:

            if vic_road_dict[volume_key] > 0:

                volume_value = volume_value + int(vic_road_dict[volume_key])

    return traffic_volume_data


def genarate_selected_volume():

    #查找需要的volume并且生成csv文件

    traffic_volume_melourne = []

    traffic_sites_melourne = []


    with open('melbourne_traffic_lights.csv', 'r', encoding='utf-8-sig') as traffic_lights_melourne:
        reader = csv.reader(traffic_lights_melourne)

        fieldnames = next(reader)
        csv_reader = csv.DictReader(traffic_lights_melourne, fieldnames=fieldnames)
        for row in csv_reader:
            dist = {}
            for k, v in row.items():
                dist[k] = v

            traffic_volume_melourne.append(dist)

    for melourne_dict in traffic_volume_melourne:

        for k, v in melourne_dict.items():

            traffic_sites_melourne_dict = {}

            if k =='SITE_NO':
                traffic_sites_melourne_dict['SITE_NO'] = melourne_dict['SITE_NO']
                traffic_sites_melourne_dict['X'] = melourne_dict['X']
                traffic_sites_melourne_dict['Y'] = melourne_dict['Y']

            traffic_sites_melourne.append(traffic_sites_melourne_dict)

    return traffic_sites_melourne


def generated_selected_file(file):

    with open(file, 'r', encoding='utf-8-sig') as traffic_volume_file:

        traffic_volume = []

        reader = csv.reader(traffic_volume_file)

        fieldnames = next(reader)
        csv_reader = csv.DictReader(traffic_volume_file, fieldnames=fieldnames)

        #在这里进行行处理
        #先删除不需要的值，在横着合并同一个字典内的数据，在合并不同字典内的数据，最后创建csv文件并些把data写入

        for row in csv_reader:
            dist = {}
            for k, v in row.items():

                dist[k] = v
            traffic_volume.append(dist)

    traffic_volume_melourne = genarate_selected_volume()

    for vic_road_dict in  traffic_volume:

       if 'NB_SCATS_SITE' in vic_road_dict:

           print('Test1')

           for melb_road_dict in traffic_volume_melourne :

               print(type(melb_road_dict))

               for keys,values in melb_road_dict.items():

                   if keys == 'SITE_NO':
                       print("Test --------------3")

                       print(type( vic_road_dict['NB_SCATS_SITE']))

                       print(type(melb_road_dict['SITE_NO']))

                       if int(vic_road_dict['NB_SCATS_SITE']) == int(melb_road_dict['SITE_NO']):
                           print("Test --------------4")

                           vic_road_dict.update(melb_road_dict)

                           with open('vic_data_melourne_2018.csv', 'a+') as vic_data_melb:

                               w = csv.writer(vic_data_melb)

                               w.writerow(vic_road_dict.values())

    print(traffic_volume)
    print('\n')


if __name__=="__main__":

    month_index = 1
    file_path = []

    days_month_31 = [1,3,5,7,8,10,12]
    days_month_30 = [4,6,9,11]
    days_month_28 = [2]

    for month_index in range(1,13,1):

        if month_index in days_month_31:
            file_path.extend(generate_file_name(month_index, 32))

        elif month_index in days_month_30:
            file_path.extend(generate_file_name(month_index, 31))

        elif month_index in days_month_28:
            file_path.extend(generate_file_name(month_index, 29))

    #file = 'vic_road_test.csv'
    #parsing_traffic_volume('vic_road_test.csv')


    for file in file_path:
        print(file)
        generated_selected_file(file)
            #parsing_traffic_volume(file)
