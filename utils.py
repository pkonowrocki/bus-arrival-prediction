import pandas as pd
import numpy as np
import os
import sys
#import geopy.distance
from warsawSectors import WarsawSectors

global_path = 'data'

debug = False

def parse_file(path_to_file):
    data = read_data(path_to_file)
    split_data_to_files(data)
    return data

def parse_folder(path_to_directory):
    print('Reading data from all files - started')
    files = os.listdir(path_to_directory)
    files = files[0:2] # todo: remove this line
    n = len(files)
    
    for i, filename in enumerate(files):
        path = f'{path_to_directory}/{filename}'
        print(f'[{i+1}/{n}] Reading data from file {path} - started')
        data = read_data(path)
        split_data_to_files(data)
        print(f'[{i+1}/{n}] Reading data from file {path} - finished')
    print('Reading data from all files - finished')
    return data

def read_data(path):
    #TODO add specific dtypes to get rid of the warning
    #dtype={"versionID": numpy.uint64}

    column_names = in_column_names()
    column_indices = range(len(column_names))
    col_idx = dict(zip(column_names, column_indices))

    indexes_of_date_columns = [col_idx['time'], col_idx['receivedTime'], col_idx['processingFinishedTime']]
    data = pd.read_csv(path, sep=';', header=None, names=col_idx.keys(), parse_dates = indexes_of_date_columns)
    
    data.drop(excluded_columns(), axis=1, inplace=True)
    data["atStop"] = data["atStop"].map({True: 1, False: 0})
    data["nearestStopDistance"] = round(data["nearestStopDistance"], 0).astype(int)
    data["previousStopDistance"] = round(data["previousStopDistance"], 0).astype(int)
    data["nextStopDistance"] = round(data["nextStopDistance"], 0).astype(int)
    # below is not needed, I leave it here in case it's useful in future
    #data["next_dist"] = distance_between_2_points(data["lon"], data["lat"], data["nearestStopLon"], data["nearestStopLat"])
    #data["sector"] = get_sectors(data["lon"], data["lat"])
    return data

def split_data_to_files(data):
    parent_directory = rf'{global_path}/lines'
    if not os.path.exists(parent_directory):
        os.makedirs(parent_directory)

    lines = data['line'].unique()
    for line in lines:

        directory = rf'{parent_directory}/{line}'
        if not os.path.exists(directory):
            os.makedirs(directory)

        data_for_line = data.loc[data['line'] == line]
        data_for_line.drop("line", axis=1, inplace=True)

        courses = data_for_line['courseID'].unique()

        for course in courses:
            data_for_course = data_for_line.loc[data_for_line['courseID'] == course]
            data_for_course.drop("courseID", axis=1, inplace=True)

            course = str(course)
            if course == 'nan':
                course = 'UNKNOWN'
            else:
                course = course.replace(' ', '')
                course = course.replace(':', '')

            filename = rf'{directory}/{line}-{course}.csv'
            # Only add headers if file does not exist yet
            headers = None if os.path.exists(filename) else out_column_names()
            data_for_course.to_csv(filename, header=headers, mode = 'a+', index=False)

def show_rows(data, amount):
    print(f'Data set size: {data.size}. First {amount} rows of data:\n')
    i = 0
    for ix, entry in data.iterrows():
        cols = ["time", "line"]
        for col in cols:
            print(entry[col])
        print('\n')
        i += 1
        if i > amount:
            break

def show_row_details(data, i):
    print("\n\nExample of full data of a row:\n")
    print(data.iloc[i])

def traverse_directory(path):
    ls = os.listdir(path)
    filenames = {key : [] for key in ls}
    for root, subdirs, files in os.walk(path, topdown=True):
        for f in files:
            filenames[os.path.basename(root)].append(f)
    return filenames

def in_column_names():
    return ["versionID", "line", "brigade", "time", "lon", "lat", "rawLon", \
                  "rawLat", "status", "delay", "delayAtStop", "plannedLeaveTime", \
                  "nearestStop", "nearestStopDistance", "nearestStopLon", \
                  "nearestStopLat", "previousStop", "previousStopLon", \
                  "previousStopLat", "previousStopDistance", "previousStopArrivalTime", \
                  "previousStopLeaveTime", "nextStop", "nextStopLon", "nextStopLat", \
                  "nextStopDistance", "nextStopTimetableVisitTime", "courseID",
                  "courseDirection", "timetableID", "timetableStatus", "receivedTime", \
                  "processingFinishedTime", "onWayToDepot", "overlapsWithNextBrigade", \
                  "overlapsWithNextBrigadeStopLineBrigade", "atStop", "speed", "oldDelay", \
                  "serverID", "delayAtStopStopSequence", "previousStopStopSequence", \
                  "nextStopStopSequence", "delayAtStopStopID", "previousStopStopID", \
                  "nextStopStopID", "coursDirectionStopStopID", "partition"]

def out_column_names():
    all_excluded_columns = excluded_columns()
    all_excluded_columns.append("line")
    all_excluded_columns.append("courseID")

    all_columns = in_column_names()
    #all_columns.append("next_dist")
    #all_columns.append("sector")
    return [item for item in all_columns if item not in all_excluded_columns]

def excluded_columns():
    return ["versionID", "brigade", "lon", "lat", "rawLon", "rawLat", "delayAtStop", "nearestStop", \
        "nearestStopLon", "nearestStopLat", "previousStop", "previousStopLon", \
        "previousStopLat", "nextStop", "nextStopLon", "nextStopLat", "courseDirection", "timetableID", \
        "receivedTime", "processingFinishedTime", "onWayToDepot", "overlapsWithNextBrigade", \
        "overlapsWithNextBrigadeStopLineBrigade", "serverID", "delayAtStopStopID", "previousStopStopID", \
        "nextStopStopID"]

def get_sectors(lat_list, lon_list):
    warsaw = WarsawSectors(debug, 10)
    result = []

    for i in range(len(lat_list)):
        if debug:
            print(f'\nIteration #{i+1}')
            if i > 10:
                exit()
        result.append(warsaw.get_sector(lat_list[i], lon_list[i]))

    return result

def distance_between_2_points(lon1, lat1, lon2, lat2):
    result = []

    for i in range(len(lat1)):
        if 0.0 in [lat1[i], lon1[i], lat2[i], lon2[i]]:
            result.append(None)
        else:
            coords_1 = (lat1[i], lon1[i])
            coords_2 = (lat2[i], lon2[i])
            result.append(geopy.distance.vincenty(coords_1, coords_2).km)

    return result