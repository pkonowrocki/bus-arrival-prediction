import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

def learn():
    filenames = traverse_directory("testing_data2/" + "/lines")
    number_of_features = 12

    model = build_model(number_of_features)

    class_names = ["late", "early", "on time"]

    for line_number, line in filenames.items():
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
