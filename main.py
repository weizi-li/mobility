
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import csv
import datetime


def dir_convert(dir):
    """convert string to int: freeway direction"""
    if dir == "N":
        return 1
    elif dir == "S":
        return 2
    elif dir == "E":
        return 3
    elif dir == "W":
        return 4
    else:
        return -1


def type_convert(type):
    """convert string to int: type of station"""
    if type == "CD":
        return 1
    elif type == "CH":
        return 2
    elif type == "FF":
        return 3
    elif type == "FR":
        return 4
    elif type == "HV":
        return 5
    elif type == "ML":
        return 6
    elif type == "OR":
        return 7
    else:
        return -1


def missing_city(s):
    if not_a_number(s[0]):
        return True
    elif float(s) < 1000:
        return True
    return False


def not_a_number(s):
    return s[0].isalpha()


def lat_range(s):
    d = float(s)
    if 30 < d < 40:
        return True
    return False


def lon_range(s):
    d = float(s)
    if -130 < d < -110:
        return True
    return False

id = []
fwy = []
dir = []
district = []
county = []
city = []
state_pm = []
abs_pm = []
latitude = []
longitude = []
length = []
type = []
lanes = []
def load_metadata(filepath):
    print(filepath)
    with open(filepath) as fp:
        count = 0
        for line in fp:
            if count > 0:  # skip the first line which contains the names for all fields
                dt = line.split()
                #print(dt[0])
                id.append(int(dt[0]))
                fwy.append(int(dt[1]))
                dir.append(dir_convert(dt[2]))
                district.append(int(dt[3]))
                county.append(int(dt[4]))

                if missing_city(dt[5]):
                     city.append(-1)
                     state_pm.append(dt[5])
                     abs_pm.append(dt[6])
                     if lat_range(dt[7]) and lon_range(dt[8]):
                        latitude.append(float(dt[7]))
                        longitude.append(float(dt[8]))
                        if not_a_number(dt[9]):
                            length.append(-1)
                            type.append(type_convert(dt[9]))
                            lanes.append(int(dt[10]))
                        else:
                            length.append(float(dt[9]))
                            type.append(type_convert(dt[10]))
                            lanes.append(int(dt[11]))
                else:
                    city.append(int(dt[5]))
                    state_pm.append(dt[6])
                    abs_pm.append(dt[7])
                    if lat_range(dt[8]) and lon_range(dt[9]):
                        latitude.append(float(dt[8]))
                        longitude.append(float(dt[9]))
                        if not_a_number(dt[10]):
                            length.append(-1)
                            type.append(type_convert(dt[10]))
                            lanes.append(int(dt[11]))
                        else:
                            length.append(float(dt[10]))
                            type.append(type_convert(dt[11]))
                            lanes.append(int(dt[12]))
            count += 1

def output_metadata(output_file):
    id_set = list(set(id))  # get unique id
    header = ['id', 'fwy', 'dir', 'district', 'county', 'city', 'state_pm', 'abs_pm', 'latitude', 'longitude', 'length',
              'type', 'lanes']
    with open(output_file, 'wt') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(header)  # write header
        for i in range(0, len(id_set)):
            idx = id.index(id_set[i])
            csv_writer.writerow([id[idx], fwy[idx], dir[idx], district[idx], county[idx], city[idx],
                                 state_pm[idx], abs_pm[idx], latitude[idx], longitude[idx],
                                 length[idx], type[idx], lanes[idx]])

def process_metadata(input_dir, output_file):
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(input_dir, filename)
            load_metadata(filepath)
        else:
            continue
    output_metadata(output_file)


def inspect_metadata(output_file):
    dt = pd.read_csv(output_file)
    # ['id', 'fwy', 'dir', 'district', 'county', 'city', 'state_pm', 'abs_pm', 'latitude', 'longitude', 'length',
    #  'type', 'lanes']
    plt.plot(dt["lanes"],'.')
    plt.show()


def process_hourdata(input_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):
            filepath = os.path.join(input_dir, filename)
            appdix = filename.find(".txt")
            output_file = filename[appdix-7:appdix] + ".csv"
            print(output_file)
            load_hourdata(filepath, output_file)
        else:
            continue


def load_hourdata(filepath, output_file):
    df = pd.read_csv(filepath, header=None, usecols=[0,1,9,11])
    header = ['id', 'flow', 'speed', 'hour', 'day', 'month', 'year', 'weekday']
    with open(output_file, 'wt') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(header)  # write header
        for i in range(len(df)):
            s = df.iloc[i,0]  # e.g., s="01/01/2019 00:00:00"
            month = int(s[0:0+2])
            day = int(s[3:3+2])
            year = int(s[6:6+4])
            hour = int(s[11:11+2])
            weekday = datetime.datetime(year,month,day).weekday()  # 0: Monday, 6: Sunday
            weekday += 1  # 1: Monday, 7: Sunday

            id = df.iloc[i,1]
            flow = df.iloc[i,2]
            speed = df.iloc[i,3]
            csv_writer.writerow([id,flow,speed,hour,day,month,year,weekday])


def output_hourdata(output_file):
    id_set = list(set(id))  # get unique id
    header = ['id', 'fwy', 'dir', 'district', 'county', 'city', 'state_pm', 'abs_pm', 'latitude', 'longitude', 'length',
              'type', 'lanes']
    with open(output_file, 'wt') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(header)  # write header
        for i in range(0, len(id_set)):
            idx = id.index(id_set[i])
            csv_writer.writerow([id[idx], fwy[idx], dir[idx], district[idx], county[idx], city[idx],
                                 state_pm[idx], abs_pm[idx], latitude[idx], longitude[idx],
                                 length[idx], type[idx], lanes[idx]])


def inspect_hourdata(filename):
    df = pd.read_csv(filename)
    eg = df.loc[df['id'] == 400007]
    plt.plot(eg["flow"])
    plt.show()


if __name__ == '__main__':

    ### processed data folder
    pf = "/home/weizili/mobility/data/processed/"

    ### for PeMS station metadata
    # input_dir = "/home/weizili/cv/data/2019-2020-station-metadata"
    # output_file = 'station-metadata-processed.csv'
    # process_metadata(input_dir, output_file)
    # inspect_metadata(output_file)

    ### for PeMS station hour data
    #input_dir = "/home/weizili/mobility/data/2019-2020-traffic-data"
    # process_hourdata(input_dir)
    inspect_hourdata(pf + "flow/2019_06.csv")

    ### for usfacts case and death data
    # input_file = "/home/weizili/mobility/data/usafacts/covid_confirmed_usafacts.csv"
    # df = pd.read_csv(input_file)
    # ca = df.loc[df['State'] == "CA"]
    # d4 = df.iloc[[193,199,213,220,230,233,235,240,241],14:14+29+31+30+31+30]  # Feb:29, Mar:31, Apr:30, May:31, Jun:30
    # d4 = d4.transpose()
    #d4.columns= ['Alameda', 'Contra Costa', 'Marin', 'Napa', 'San Francisco',
    #           'San Mateo', 'Santa Clara', 'Solano', 'Sonoma']
    # d4.columns= [1, 13, 41, 55, 75, 81, 85, 95, 97]
    # d4.to_csv("case-0201-0630.csv", index=False)
    # case = pd.read_csv("case-0201-0630.csv")
    # death = pd.read_csv("death-0201-0630.csv")
    # plt.plot(death["Alameda"] / case["Alameda"])
    # plt.plot(death["Sonoma"] / case["Sonoma"])
    # plt.show()

    # df = pd.read_csv(pf + "station-metadata.csv")
    # print(df.loc[df["county"]==55])

