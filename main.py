import pandas as pd
import numpy as np

def main():
    path = "data/2018-05-21/part-0-0"
    data = readData(path)
    showRows(data, amount=10)
    showRowDetails(data, i=0)

def readData(path):
    #TODO add specific dtypes to get rid of the warning
    #dtype={"versionID": numpy.uint64}
    columnNames = ["versionID", "line", "brigade", "time", "lon", "lat", "rawLon", \
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
    columnIndices = range(len(columnNames))
    col_idx = dict(zip(columnNames, columnIndices))

    indexesOfDateColumns = [col_idx['time'], col_idx['receivedTime'], col_idx['processingFinishedTime']]
    data = pd.read_csv(path, sep=';', header=None, names=col_idx.keys(), \
        parse_dates = indexesOfDateColumns)

    data = data.sort_values(by=['line', 'brigade', 'time'], ascending=True)
    return data

def showRows(data, amount):
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

def showRowDetails(data, i):
    print('\n\nExample of full data of a row:\n')
    print(data.iloc[i])

if __name__ == "__main__":
    main()