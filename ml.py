import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import seaborn as sns
import matplotlib.pyplot as plt
from utils import traverse_directory
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

def hashmap_to_single_df(filenames):
    csvs = []
    for line_number, list_of_lines in filenames.items():
        for line in list_of_lines:
            data = pd.read_csv('testing_data2/lines/' + line_number + \
                                            '/' + line)
            csvs.append(data)
    return pd.concat(csvs)

def learn():
    filenames = traverse_directory("testing_data2/" + "/lines")
    df = hashmap_to_single_df(filenames)

    number_of_features = 12

    model = build_model(number_of_features)

    class_names = ["late", "early", "on time"]

    #df.dropna()
    #df.pop("time")
    #df.pop("plannedLeaveTime")
    #df.pop("previousStopArrivalTime")
    #df.pop("previousStopLeaveTime")
    #df.pop("nextStopTimetableVisitTime")
    
    training_datafiles, testing_datafiles = train_test_split(df, test_size=0.3)
    #train_labels = train_dataset.pop("delay_status")

    #model.fit(train_dataset, train_labels, epochs=10, verbose=1)

    test_labels = test_dataset.pop("delay_status")

    #test_loss, test_acc = model.evaluate(test_dataset, test_labels)

    #print('\nTest accuracy:', test_acc)

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
