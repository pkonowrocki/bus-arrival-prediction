import pandas as pd
import numpy as np
import os
import sys

global_path = 'data'

def get_column_names():
    return ["versionID", "line", "brigade", "time", "lon", "lat", "rawLon", \
                  "rawLat", "status", "delay", "delayAtStop", "plannedLeaveTime", \
                  "nearestStop", "nearestStopDistance", "nearestStopLon", \
                  "nearestStopLat", "previousStop", "previousStopLon", \
                  "previousStopLat", "previousStopDistance", "previousStopArrivalTime", \
                  "previousStopLeaveTime", "nextStop", "nextStopLon", "nextStopLat", \
                  "nextStopDistance", "nextStopTimetableVisitTime", "courseID", \
                  "courseDirection", "timetableID", "timetableStatus", "receivedTime", \
                  "processingFinishedTime", "onWayToDepot", "overlapsWithNextBrigade", \
                  "overlapsWithNextBrigadeStopLineBrigade", "atStop", "speed", "oldDelay" \
                  "serverID", "delayAtStopStopSequence", "previousStopStopSequence", \
                  "nextStopStopSequence", "delayAtStopStopID", "previousStopStopID", \
                  "nextStopStopID", "coursDirectionStopStopID", "partition"]

def main():
    # Read single file
    #data = parse_file(global_path + '/2018-05-21/part-0-0')

    # Read all files in one directory
    parse_folder(global_path + '/2018-05-21')

    # show_rows(data, amount=10)
    # show_row_details(data, i=0)

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

def read_data(path):
    #TODO add specific dtypes to get rid of the warning
    #dtype={"versionID": numpy.uint64}

    column_names = get_column_names()
    column_indices = range(len(column_names))
    col_idx = dict(zip(column_names, column_indices))

    indexes_of_date_columns = [col_idx['time'], col_idx['receivedTime'], col_idx['processingFinishedTime']]
    data = pd.read_csv(path, sep=';', header=None, names=col_idx.keys(), \
        parse_dates = indexes_of_date_columns)

    data = data.sort_values(by=['line', 'brigade', 'time'], ascending=True)
    return data

def split_data_to_files(data):
    directory = rf'{global_path}/lines'
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    lines = data['line'].unique()
    for line in lines:
        filename = rf'{directory}/{line}.csv'
        # Only add headers if file does not exist yet
        headers = None if os.path.exists(filename) else get_column_names()
        data_for_line = data.loc[data['line'] == line]
        data_for_line.to_csv(filename, header=headers, mode = 'a+')

def show_rows(data, amount):
    print(f'Data set size: {data.size}. First {amount} rows of data:\n')
    i = 0
    for ix, entry in data.iterrows():
        cols = ['time', 'line', 'brigade']
        for col in cols:
            print(entry[col])
        print('\n')
        i += 1
        if i > amount:
            break

def show_row_details(data, i):
    print('\n\nExample of full data of a row:\n')
    print(data.iloc[i])

if __name__ == "__main__":
    main()
