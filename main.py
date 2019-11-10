import pandas as pd
import numpy as np
import os
import sys

global_path = '/home/tpalayda/Desktop/studying/ppd/project/'

def main():
    path = global_path + '/2018-05-26/part-0-0'
    data = read_data(path)

    split_data_to_files(data)

    show_rows(data, amount=10)
    show_row_details(data, i=0)

def read_data(path):
    #TODO add specific dtypes to get rid of the warning
    #dtype={"versionID": numpy.uint64}
    column_names = ["versionID", "line", "brigade", "time", "lon", "lat", "rawLon", \
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

    column_indices = range(len(column_names))
    col_idx = dict(zip(column_names, column_indices))

    indexes_of_date_columns = [col_idx['time'], col_idx['receivedTime'], col_idx['processingFinishedTime']]
    data = pd.read_csv(path, sep=';', header=None, names=col_idx.keys(), \
        parse_dates = indexes_of_date_columns)

    data = data.sort_values(by=['line', 'brigade', 'time'], ascending=True)
    return data


def split_data_to_files(data):
    directory = rf'{global_path}/lines'
    print(f'Splitting data by line and saving it in {directory} - started.')
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    lines = data['line'].unique()
    for line in lines:
        data_for_line = (data['line'] == line)
        data_for_line.to_csv(rf'{directory}/{line}.csv', header=False, mode = 'a+')
    print(f'Splitting data by line and saving it in {directory} - finished.')


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
