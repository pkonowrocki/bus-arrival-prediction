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

def is_non_zero_file(path):  
    return os.path.isfile(path) and os.path.getsize(path) > 0

# filenames is hashmap in form of -> line (string) : list (list of strings)
def all_csv_to_single_csv(path_to_traverse, filename):
    filenames = traverse_directory(path_to_traverse)
    csvs = []
    for line_number, list_of_lines in filenames.items():
        for line in list_of_lines:
            path = path_to_traverse + '/' + line_number + '/' + line
            if is_non_zero_file(path):
                print("Processing: " + path)
                data = pd.read_csv(path, header=None)
                csvs.append(data)
    df = pd.concat(csvs)
    df.to_csv(filename, index=False, header=False)

def convert_all_csv(path_to_traverse, path_to_save):
    filenames = traverse_directory(path_to_traverse)
    csvs = []

    for line_number, list_of_lines in filenames.items():
        if not os.path.exists(path_to_save + "/" + line_number):
            os.makedirs(path_to_save + "/" + line_number)

        for line in list_of_lines:
            path = path_to_traverse + "/" + line_number + "/" + line
            changed_path = path_to_save + "/" + line_number + "/" + line


            data = pd.read_csv(path)
            convert_single_csv(data, changed_path)
            print("Reading file from path: ", path)

def convert_single_csv(df, path):
    labels = df.pop("delay_status").values.tolist()
    list_of_lists = df.values.tolist()
    data = []

    for i in range(len(list_of_lists)):
        current_row = list_of_lists[i]
        if(i+2 < len(list_of_lists)):
            next_row = list_of_lists[i+1]
            next_next_row = list_of_lists[i+2]
            label = labels[i+2]
            data.append(current_row + next_row + next_next_row + [label])

    df2 = pd.DataFrame.from_records(data)
    df2.to_csv(path, index=False, header=False)
    print("Saved to path: ", path)

def count_delay_statuses(df):
    zeros = len(df.loc[df["delay_status"] == 0])
    ones = len(df.loc[df["delay_status"] == 1])
    twos = len(df.loc[df["delay_status"] == 2])

    n = len(df.index)
    print("--------------------------")
    print("delay_status == 0: ", 100 * zeros / n)
    print("delay_status == 1: ", 100 * ones / n)
    print("delay_status == 2: ", 100 * twos / n)
    print("--------------------------")

def parse_file(path_to_file):
    data = read_data(path_to_file)
    split_data_to_files(data)
    return data

def create_single_file(path_to_directory, with_old_delay):
    parse_folder(path_to_directory, with_old_delay, is_one_file=True)

def parse_folder(path_to_directory, with_old_delay, is_one_file=False):
    print('Reading data from all files - started')
    files = os.listdir(path_to_directory)
    n = len(files)
    
    for i, filename in enumerate(files):
        path = f'{path_to_directory}/{filename}'
        print(f'[{i+1}/{n}] Reading data from file {path} - started')
        data = read_data(path, with_old_delay)
        if not is_one_file:
            split_data_to_files(data, "normal", out_column_names(with_old_delay))
        else:
            save_data_to_one_file(data, with_old_delay)
        print(f'[{i+1}/{n}] Reading data from file {path} - finished')
    print('Reading data from all files - finished')
    return data

def parse_folder_PCA(path_to_directory, with_old_delay):
    print('Reading data from all files - started')
    files = os.listdir(path_to_directory)
    n = len(files)
    data = None

    for i, filename in enumerate(files):
        path = f'{path_to_directory}/{filename}'
        print(f'[{i+1}/{n}] Reading data from file {path} - started')
        if data is None:
            data = read_data(path, with_old_delay)
        else:
            data = data.append(read_data(path, with_old_delay), ignore_index=True)
        print(f'[{i+1}/{n}] Reading data from file {path} - finished')
    print('Reading data from all files - finished')

    data.dropna(inplace=True)

    data_for_PCA = data.drop(["delay_status", "courseID"], axis=1)

    print('Processing - started')
    data_scaled = StandardScaler().fit_transform(data_for_PCA)
    principalComponents = PCA(n_components=9).fit_transform(data_scaled)
    PCA_columns = ['PC1', 'PC2', 'PC3', 'PC4', 'PC5', 'PC6', 'PC7', 'PC8', 'PC9']
    principalDf = pd.DataFrame(data=principalComponents, columns=PCA_columns)
    principalDf["delay_status"] = data["delay_status"].values
    principalDf["line"] = data["line"].values
    principalDf["courseID"] = data["courseID"].values
    PCA_columns.extend(["delay_status"])
    print('Processing - finished')

    print('Saving to file - started')
    split_data_to_files(principalDf, "PCA", PCA_columns, is_PCA=True)
    print('Saving to file - finished')

def read_data(path, with_old_delay):
    #TODO add specific dtypes to get rid of the warning
    #dtype={"versionID": numpy.uint64}

    column_names = in_column_names()
    column_indices = range(len(column_names))
    col_idx = dict(zip(column_names, column_indices))

    indexes_of_date_columns = [col_idx['time'], col_idx['plannedLeaveTime'], col_idx['previousStopArrivalTime'], \
        col_idx['previousStopLeaveTime'], col_idx['nextStopTimetableVisitTime']]
    data = pd.read_csv(path, sep=';', header=None, names=col_idx.keys(), parse_dates = indexes_of_date_columns)
    
    data.drop(excluded_columns(), axis=1, inplace=True)
    if not with_old_delay:
        data.drop("oldDelay", axis=1, inplace=True)
    data["line"] = get_line(data["line"])
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
    data.drop("delay", axis=1, inplace=True)
    # below is not needed, I leave it here in case it's useful in future
    #data["next_dist"] = distance_between_2_points(data["lon"], data["lat"], data["nearestStopLon"], data["nearestStopLat"])
    #data["sector"] = get_sectors(data["lon"], data["lat"])
    return data

def split_data_to_files(data, type, column_names, is_PCA=False):
    parent_directory = rf'{global_path}/lines-{type}'
    if not os.path.exists(parent_directory):
        os.makedirs(parent_directory)

    lines = data['line'].unique()
    for line in lines:

        directory = rf'{parent_directory}/{line}'
        if not os.path.exists(directory):
            os.makedirs(directory)

        data_for_line = data.loc[data['line'] == line]
        if is_PCA:
            data_for_line.drop("line", axis=1, inplace=True)

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

def save_data_to_one_file(data, with_old_delay):
    data.drop("courseID", axis=1, inplace=True)
    data.drop("delay_status", axis=1, inplace=True)

    filename = rf'{global_path}/all.csv'
    headers = None if os.path.exists(filename) else out_column_names(with_old_delay, is_one_file = True)
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

def out_column_names(with_old_delay, is_one_file = False):
    all_excluded_columns = excluded_columns()
    all_excluded_columns.extend(["time", "plannedLeaveTime", "previousStopArrivalTime", "previousStopLeaveTime", "nextStopTimetableVisitTime"])
    all_excluded_columns.append("courseID")
    all_excluded_columns.append("delay")
    if not with_old_delay:
        all_excluded_columns.append("oldDelay")

    all_columns = in_column_names()
    all_columns.extend(["time_h", "time_m", "plannedLeaveTime_h", "plannedLeaveTime_m",
     "previousStopArrivalTime_h", "previousStopArrivalTime_m", "previousStopLeaveTime_h",
     "previousStopLeaveTime_m", "nextStopTimetableVisitTime_h", "nextStopTimetableVisitTime_m"])
    #all_columns.append("next_dist")
    #all_columns.append("sector")
    if not is_one_file:
        all_columns.append("delay_status")
    return [item for item in all_columns if item not in all_excluded_columns]

def excluded_columns():
    return ["versionID", "brigade", "lon", "lat", "rawLon", "rawLat", "delayAtStop", "nearestStop", \
        "nearestStopLon", "nearestStopLat", "previousStop", "previousStopLon", \
        "previousStopLat", "nextStop", "nextStopLon", "nextStopLat", "courseDirection", "timetableID", \
        "receivedTime", "processingFinishedTime", "onWayToDepot", "overlapsWithNextBrigade", \
        "overlapsWithNextBrigadeStopLineBrigade", "serverID", "delayAtStopStopID", "previousStopStopID", \
        "nextStopStopID", "courseDirectionStopStopID", "partition"]

def get_line(line_list):
    result = []
    for line in line_list:
        if line[0].isnumeric():
            single_result = line
        else:
            if line == 'Z':
                single_result = 999
            elif line[1].isnumeric() and line[1] is not '0':
                single_result = int(line[1:])
            else:
                single_result =  int(line[2:]) if line[2:].isnumeric() else None

            if single_result == 'L':
                single_result = 998
        result.append(single_result)
    return result

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
        if delay > 120:
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
