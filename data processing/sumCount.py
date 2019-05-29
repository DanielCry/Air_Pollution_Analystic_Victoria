import csv
import io
import os
import regex as re

#filePath = "vic_road_test.csv"
fileName=''

def readFile(filePath):
    with io.open(filePath, 'r', encoding='utf-8-sig') as volume_data:
        reader = csv.reader(volume_data)

        trafficVolumns = []
        fieldnames = next(reader)
        csv_reader = csv.DictReader(volume_data, fieldnames=fieldnames)

        for row in csv_reader:
            dic = {}

            for index in range(0, 96):
                volume_key = "V" + "{0:0=2d}".format(index)
                if row[volume_key] == '':

                    row[volume_key] = 0

                if int(row[volume_key]) < 0:
                    row[volume_key] = 0

            for k, v in row.items():
                dic[k] = v

            trafficVolumns.append(dic)

        return (processLine(trafficVolumns))


def processLine(trafficVolumns):
    processedLines = []
    for line in trafficVolumns:
        processedLine = {'NB_SCATS_SITE': int(line['NB_SCATS_SITE']), 'QT_INTERVAL_COUNT': line['QT_INTERVAL_COUNT'],
        1: int(line['V00']) + int(line['V01']) + int(line['V02']) +  int(line['V03']),
        2: int(line['V04']) + int(line['V05']) + int(line['V06']) + int(line['V07']) ,
        3: int(line['V08']) + int(line['V09']) + int(line['V10']) + int(line['V11']),
        4: int(line['V12']) + int(line['V13']) + int(line['V14']) + int(line['V15']),
        5: int(line['V16']) + int(line['V17']) + int(line['V18']) + int(line['V19']),
        6: int(line['V20']) + int(line['V21']) + int(line['V22']) + int(line['V23']),
        7: int(line['V24']) + int(line['V25']) + int(line['V26']) + int(line['V27']),
        8: int(line['V28']) + int(line['V29']) + int(line['V30']) + int(line['V31']),
        9: int(line['V32']) + int(line['V33']) + int(line['V34']) + int(line['V35']),
        10: int(line['V36']) + int(line['V37']) + int(line['V38']) + int(line['V39']),
        11: int(line['V40']) + int(line['V41']) + int(line['V42']) + int(line['V43']),
        12: int(line['V44']) + int(line['V45']) + int(line['V46']) + int(line['V47']),
        13: int(line['V48']) + int(line['V49']) + int(line['V50']) + int(line['V51']),
        14: int(line['V52']) + int(line['V53']) + int(line['V54']) + int(line['V55']),
        15: int(line['V56']) + int(line['V57']) + int(line['V58']) + int(line['V59']),
        16: int(line['V60']) + int(line['V61']) + int(line['V62']) + int(line['V63']),
        17: int(line['V64']) + int(line['V65']) + int(line['V66']) + int(line['V67']),
        18: int(line['V68']) + int(line['V69']) + int(line['V70']) + int(line['V71']),
        19: int(line['V72']) + int(line['V73']) + int(line['V74']) + int(line['V75']),
        20: int(line['V76']) + int(line['V77']) + int(line['V78']) + int(line['V79']),
        21: int(line['V80']) + int(line['V81']) + int(line['V82']) + int(line['V83']),
        22: int(line['V84']) + int(line['V85']) + int(line['V86']) + int(line['V87']),
        23: int(line['V88']) + int(line['V89']) + int(line['V90']) + int(line['V91']),
        24: int(line['V92']) + int(line['V93']) + int(line['V94']) + int(line['V95']),
        'NM_REGION': line['NM_REGION'], 'CT_RECORDS': line['CT_RECORDS'], 
        'QT_VOLUME_24HOUR': line['QT_VOLUME_24HOUR'], 'CT_ALARM_24HOUR': line['CT_ALARM_24HOUR']}
        #print(processedLine)
        processedLines.append(processedLine)
    #print (len(processedLines))
    return(processedLines)

def gatherLine(file):

    lines = readFile(file)

    gatheredLines = []
    i = 0
    for line in lines:
        line['id'] = i
        i += 1

    for line in lines:

        lines.remove(line)
        #print ([i['id'] for i in lines])

        templines = lines[:]
        for tempLine in templines:
            if tempLine['NB_SCATS_SITE'] == line['NB_SCATS_SITE']:
                lines.remove(tempLine)
                #print(tempLine['id'])
                index = 1
                while index < 25:
                    #print(index)
                    line[index] = line[index] + tempLine[index]
                    #print (processedLine[index])
                    index += 1

        gatheredLines.append(line)
    #print (gatheredLines)
    return gatheredLines


def readAllFile():
    files=os.listdir('toBeProcessed') 
    
    for file in files:
        fileName = file.split('/')[-1]
        #print (fileName)
        file = 'toBeProcessed/' + file
        tobeWriten = gatherLine(file)
        writePath = 'Processed/' + fileName
        #os.mkdir(writePath)
        with open(writePath, 'a+', newline = '') as f:
            w = csv.writer(f)
            for row in tobeWriten:
                w.writerow(row.values())

#gatherLine()
readAllFile()    

            




