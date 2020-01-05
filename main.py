from utils import *
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import seaborn as sns
import matplotlib.pyplot as plt


global_path = 'testing_data'

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
    filenames = traverse_directory(global_path + "/lines")

    line_157 = filenames["157"]

    testing_data = []
    training_data = []

    for i, filename in enumerate(line_157):
        if(i % 4 == 0):
            testing_data.append(filename)
        else:
            training_data.append(filename)

    train_dataset = pd.read_csv('testing_data/lines/157/' + training_data[0])
    test_dataset = pd.read_csv('testing_data/lines/157/' + testing_data[0])
    
    train_dataset.dropna()
    test_dataset.dropna()

    train_dataset.pop("time")
    train_dataset.pop("plannedLeaveTime")
    train_dataset.pop("previousStopArrivalTime")
    train_dataset.pop("previousStopLeaveTime")
    train_dataset.pop("nextStopTimetableVisitTime")

    test_dataset.pop("time")
    test_dataset.pop("plannedLeaveTime")
    test_dataset.pop("previousStopArrivalTime")
    test_dataset.pop("previousStopLeaveTime")
    test_dataset.pop("nextStopTimetableVisitTime")

    train_labels = train_dataset.pop("delay_status")
    test_labels = test_dataset.pop("delay_status")
    class_names = ["late", "early", "on time"]

    model = build_model(len(train_dataset.keys()))

    model.fit(train_dataset, train_labels, epochs=10)

    test_loss, test_acc = model.evaluate(test_dataset, test_labels, verbose=2)

    print('\nTest accuracy:', test_acc)

    #sns.pairplot(df[["delay", "time", "plannedLeaveTime", "nearestStopDistance", "speed", "nextStopDistance"]], diag_kind="kde")
    #plt.show()
    
if __name__ == "__main__":
    main()
