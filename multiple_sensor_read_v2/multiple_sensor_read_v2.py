# This version differs in that instead of accessing the API of each photon
# individually, we instead "subscribe" to the data that is being published
# from the dashboard. (https://api.particle.io/v1/devices/events?access_token=e3b97b631ba672639adb56987eae0c3015fd5dda)

# Got code to print out data from user Jay L (http://stackoverflow.com/questions/29550426/how-to-parse-output-from-sse-client-in-python)

import sseclient
import pandas as pd
import csv
import requests, json
import time
import datetime

#Global definitions
access_token = 'e3b97b631ba672639adb56987eae0c3015fd5dda'
particle_url = 'https://api.particle.io/v1/devices/events?access_token=' + access_token
starttime = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
filename = starttime+"datalogger_test.csv"

dataIndex = []
nameIndex = []

stopWrite = False

messages = sseclient.SSEClient(particle_url)
with open(filename, "a") as file:
    writer = csv.writer(file, delimiter = ",")
    for msg in messages:

        #prints out the event
        event = str(msg.event)
        #print event + str(nameIndex[0])
        if nameIndex:
            if event == nameIndex[0]:
                if stopWrite == False: #This is so it only prints once
                    writer.writerow(nameIndex)
                    stopWrite = True
                writer.writerow(dataIndex)
                dataIndex = []

        if event != 'message':
            print event
            nameIndex.append(event)

        #prints out the data
        outputMsg = msg.data
        if type(outputMsg) is not str:
            data_json = json.loads(outputMsg)
            parse_data = str(data_json['data'])
            dataIndex.append(parse_data)
            print parse_data
            