import pandas as pd
import numpy as np
import os
import sys
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
#import geopy.distance
from warsawSectors import WarsawSectors

global_path = 'data'

debug = False

def parse_file(path_to_file):
    data = read_data(path_to_file)
    split_data_to_files(data)
    return data

def create_single_file(path_to_directory):
    parse_folder(path_to_directory, is_one_file=True)

def parse_folder(path_to_directory, is_one_file=False):
    print('Reading data from all files - started')
    files = os.listdir(path_to_directory)
    files = files[0:2]
    n = len(files)
    
    for i, filename in enumerate(files):
        path = f'{path_to_directory}/{filename}'
        print(f'[{i+1}/{n}] Reading data from file {path} - started')
        data = read_data(path)
        if not is_one_file:
            split_data_to_files(data, "normal", out_column_names())
        else:
            save_data_to_one_file(data)
        print(f'[{i+1}/{n}] Reading data from file {path} - finished')
    print('Reading data from all files - finished')
    return data

def parse_folder_PCA(path_to_directory):
    print('Reading data from all files - started')
    files = os.listdir(path_to_directory)
    files = files[0:2]
    n = len(files)
    data = None

    for i, filename in enumerate(files):
        path = f'{path_to_directory}/{filename}'
        print(f'[{i+1}/{n}] Reading data from file {path} - started')
        if data is None:
            data = read_data(path)
        else:
            data = data.append(read_data(path), ignore_index=True)
        print(f'[{i+1}/{n}] Reading data from file {path} - finished')
    print('Reading data from all files - finished')

    data.dropna(inplace=True)

    data_for_PCA = data.drop(["delay_status", "line", "courseID"], axis=1)

    print('Processing - started')
    data_scaled = StandardScaler().fit_transform(data_for_PCA)
    principalComponents = PCA(n_components=9).fit_transform(data_scaled)
    PCA_columns = ['PC1', 'PC2', 'PC3', 'PC4', 'PC5', 'PC6', 'PC7', 'PC8', 'PC9']
    principalDf = pd.DataFrame(data=principalComponents, columns=PCA_columns)
    principalDf["delay_status"] = data["delay_status"].values
    principalDf["line"] = data["line"].values
    principalDf["courseID"] = data["courseID"].values
    PCA_columns.extend(["delay_status", "line"])
    print('Processing - finished')

    print('Saving to file - started')
    split_data_to_files(principalDf, "PCA", PCA_columns)
    print('Saving to file - finished')

def read_data(path):
    #TODO add specific dtypes to get rid of the warning
    #dtype={"versionID": numpy.uint64}

    column_names = in_column_names()
    column_indices = range(len(column_names))
    col_idx = dict(zip(column_names, column_indices))

    indexes_of_date_columns = [col_idx['time'], col_idx['plannedLeaveTime'], col_idx['previousStopArrivalTime'], \
        col_idx['previousStopLeaveTime'], col_idx['nextStopTimetableVisitTime']]
    data = pd.read_csv(path, sep=';', header=None, names=col_idx.keys(), parse_dates = indexes_of_date_columns)
    
    data.drop(excluded_columns(), axis=1, inplace=True)
    data["status"] = data["status"].map({'UNKNOWN': None, 'STOPPED': 0, 'MOVING_SLOWLY': 1, 'MOVING': 2})
    data["timetableStatus"] = data["timetableStatus"].map({'UNSAFE': 0, 'SAFE': 1})
    data["time_h"] = get_time(data["time"], "%H")
    data["time_m"] = get_time(data["time"], "%M")
    data["plannedLeaveTime_h"] = get_time(data["plannedLeaveTime"], "%H")
    data["plannedLeaveTime_m"] = get_time(data["plannedLeaveTime"], "%M")
    data["previousStopArrivalTime_h"] = get_time(data["previousStopArrivalTime"], "%H")
    data["previousStopArrivalTime_m"] = get_time(data["previousStopArrivalTime"], "%M")
    data["previousStopLeaveTime_h"] = get_time(data["previousStopLeaveTime"], "%H")
    data["previousStopLeaveTime_m"] = get_time(data["previousStopLeaveTime"], "%M")
    data["nextStopTimetableVisitTime_h"] = get_time(data["nextStopTimetableVisitTime"], "%H")
    data["nextStopTimetableVisitTime_m"] = get_time(data["nextStopTimetableVisitTime"], "%M")
    data.drop(["time", "plannedLeaveTime", "previousStopArrivalTime", "previousStopLeaveTime", "nextStopTimetableVisitTime"], axis=1, inplace=True)
    data["atStop"] = data["atStop"].map({True: 1, False: 0})
    data["nearestStopDistance"] = round(data["nearestStopDistance"], 0).astype(int)
    data["previousStopDistance"] = round(data["previousStopDistance"], 0).astype(int)
    data["nextStopDistance"] = round(data["nextStopDistance"], 0).astype(int)
    data["delay_status"] = get_delay_status(data["delay"])
    # below is not needed, I leave it here in case it's useful in future
    #data["next_dist"] = distance_between_2_points(data["lon"], data["lat"], data["nearestStopLon"], data["nearestStopLat"])
    #data["sector"] = get_sectors(data["lon"], data["lat"])
    return data

def split_data_to_files(data, type, column_names):
    parent_directory = rf'{global_path}/lines-{type}'
    if not os.path.exists(parent_directory):
        os.makedirs(parent_directory)

    lines = data['line'].unique()
    for line in lines:

        directory = rf'{parent_directory}/{line}'
        if not os.path.exists(directory):
            os.makedirs(directory)

        data_for_line = data.loc[data['line'] == line]

        courses = data_for_line['courseID'].unique()

        for course in courses:
            data_for_course = data_for_line.loc[data_for_line['courseID'] == course]
            data_for_course.drop("courseID", axis=1, inplace=True)

            course = str(course)
            if course == 'nan':
                continue
            else:
                course = course.replace(' ', '')
                course = course.replace(':', '')

            filename = rf'{directory}/{line}-{course}.csv'
            # Only add headers if file does not exist yet
            headers = None if os.path.exists(filename) else column_names
            data_for_course.to_csv(filename, header=headers, mode = 'a+', index=False)

def save_data_to_one_file(data):
    data.drop("courseID", axis=1, inplace=True)

    filename = rf'{global_path}/all.csv'
    headers = out_column_names(is_one_file = True)
    data.to_csv(filename, header=headers, mode = 'a+', index=False)

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
                  "nextStopStopID", "courseDirectionStopStopID", "partition"]

def out_column_names(is_one_file = False):
    all_excluded_columns = excluded_columns()
    all_excluded_columns.extend(["time", "plannedLeaveTime", "previousStopArrivalTime", "previousStopLeaveTime", "nextStopTimetableVisitTime"])
    all_excluded_columns.append("courseID")

    all_columns = in_column_names()
    all_columns.extend(["time_h", "time_m", "plannedLeaveTime_h", "plannedLeaveTime_m",
     "previousStopArrivalTime_h", "previousStopArrivalTime_m", "previousStopLeaveTime_h",
     "previousStopLeaveTime_m", "nextStopTimetableVisitTime_h", "nextStopTimetableVisitTime_m"])
    #all_columns.append("next_dist")
    #all_columns.append("sector")
    all_columns.append("delay_status")
    return [item for item in all_columns if item not in all_excluded_columns]

def excluded_columns():
    return ["versionID", "brigade", "lon", "lat", "rawLon", "rawLat", "delayAtStop", "nearestStop", \
        "nearestStopLon", "nearestStopLat", "previousStop", "previousStopLon", \
        "previousStopLat", "nextStop", "nextStopLon", "nextStopLat", "courseDirection", "timetableID", \
        "receivedTime", "processingFinishedTime", "onWayToDepot", "overlapsWithNextBrigade", \
        "overlapsWithNextBrigadeStopLineBrigade", "serverID", "delayAtStopStopID", "previousStopStopID", \
        "nextStopStopID", "courseDirectionStopStopID", "partition"]

def get_time(date_time_list, format):
    result = []
    for date_time in date_time_list:
        if issubclass(type(date_time), type(pd.NaT)):
            # TODO: maybe we should calculate value based on neighbors
            result.append(None)
        else:
            time = date_time.strftime(format)
            if time[0] == '0':
                time = time[1:]
            result.append(time)
    return result

def get_delay_status(delay_list):
    result = []

    for delay in delay_list:
        if delay > 180:
            result.append(2)
        elif delay < -60:
            result.append(1)
        else:
            result.append(0)
    return result

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
