from utils import *
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
from sklearn.model_selection import train_test_split

global_path = 'data'

def build_model(input_shape):
    model = keras.Sequential([
        layers.Dense(64, activation='relu', 
            input_shape=[input_shape]),
        layers.Dense(3, activation='softmax'),
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    return model

def norm(x, stats):
    return (x - stats['mean']) / stats['std']

def plot_data(df: pd.DataFrame):
    sns.pairplot(df[["delay", "time", "plannedLeaveTime", "nearestStopDistance",
                     "speed", "nextStopDistance"]], diag_kind="kde")
    plt.show()

def timestamp_to_int(timestamp: str):
    date_string = dt.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
    return int(dt.datetime.strftime(date_string, '%m%d%H'))

def main():
    # Read single file
    #data = parse_file(global_path + '/2018-05-26/part-0-0')

    # Read all files in one directory
    #is_one_file = True
    #data = parse_folder(global_path + '/2018-05-21', is_one_file)
    #data = parse_folder(global_path + '/2018-05-26/')

    # show_rows(data, amount=10)
    # show_row_details(data, i=0)

    # filenames is hashmap in form of -> line (string) : list (list of strings)
    
    filenames = traverse_directory("testing_data2/" + "/lines")
    number_of_features = 17

    model = build_model(number_of_features)

    class_names = ["late", "early", "on time"]

    d = {'157': filenames["157"]} # just for testing purposes

    train_dataset = pd.read_csv('testing_data2/lines/' + "157" + \
                                '/' + d["157"][0])
    test_dataset = pd.read_csv('testing_data2/lines/' + "157" + \
                                '/' + d["157"][1])

    train_dataset.dropna()
    test_dataset.dropna()
    
    train_dataset["time"] = pd.to_datetime(train_dataset["time"]).astype(int)
    train_dataset["plannedLeaveTime"] = pd.to_datetime(train_dataset["time"]).astype(int)
    train_dataset["previousStopArrivalTime"] = pd.to_datetime(train_dataset["time"]).astype(int)
    train_dataset["previousStopLeaveTime"] = pd.to_datetime(train_dataset["time"]).astype(int)
    train_dataset["nextStopTimetableVisitTime"] = pd.to_datetime(train_dataset["time"]).astype(int)

    test_dataset["time"] = pd.to_datetime(train_dataset["time"]).astype(int)
    test_dataset["plannedLeaveTime"] = pd.to_datetime(train_dataset["time"]).astype(int)
    test_dataset["previousStopArrivalTime"] = pd.to_datetime(train_dataset["time"]).astype(int)
    test_dataset["previousStopLeaveTime"] = pd.to_datetime(train_dataset["time"]).astype(int)
    test_dataset["nextStopTimetableVisitTime"] = pd.to_datetime(train_dataset["time"]).astype(int)

    test_dataset["delay_status"] = train_dataset["delay_status"] + 1

    # one hot encoding -- maybe later
    #train_dataset["delay_status"] = train_dataset["delay_status"].map(lambda x: 
    #                                {1: 'ONTIME', 2: 'EARLY', 3: 'LATE'}.get(x))

    #train_dataset = pd.get_dummies(train_dataset, prefix='', prefix_sep='', 
    #                               columns="delay_status")

    #print(train_dataset.tail())

    #print(train_dataset.describe())
    train_dataset = norm(train_dataset, train_dataset.describe().transpose())

    train_dataset["delay_status"] = 1
    train_dataset["timetableStatus"] = 1

    #print(train_dataset)
    #plot_data(train_dataset)

    train_labels = train_dataset.pop("delay_status")
    test_labels = test_dataset.pop("delay_status")
    
    for row in train_dataset.iterrows():
        print(row)
    
    model.fit(train_dataset, train_labels, epochs=10, verbose=1)

    #test_loss, test_acc = model.evaluate(test_dataset, test_labels)
    predictions = model.predict(test_dataset)
    print(predictions[0])
    print(np.argmax(predictions[0]))
    print(test_labels[0])



    #print('\nTest accuracy:', test_acc)

    '''
    for line_number, line in d.items():
        training_datafiles, testing_datafiles = train_test_split(line, test_size=0.3)

        for training_datafile in training_datafiles:
            train_dataset = pd.read_csv('testing_data2/lines/' + line_number + \
                                        '/' + training_datafile)

            train_dataset.dropna()
            train_dataset.pop("time")
            train_dataset.pop("plannedLeaveTime")
            train_dataset.pop("previousStopArrivalTime")
            train_dataset.pop("previousStopLeaveTime")
            train_dataset.pop("nextStopTimetableVisitTime")


            train_labels = train_dataset.pop("delay_status")
            model.fit(train_dataset, train_labels, epochs=10, verbose=1)

        for testing_datafile in testing_datafiles:
            test_dataset = pd.read_csv('testing_data2/lines/' + line_number + \
                                        '/' + testing_datafile)
            test_dataset.dropna()
            test_dataset.pop("time")
            test_dataset.pop("plannedLeaveTime")
            test_dataset.pop("previousStopArrivalTime")
            test_dataset.pop("previousStopLeaveTime")
            test_dataset.pop("nextStopTimetableVisitTime")
            test_labels = test_dataset.pop("delay_status")

            test_loss, test_acc = model.evaluate(test_dataset, test_labels)

            print('\nTest accuracy:', test_acc)
    '''

if __name__ == "__main__":
    main()
