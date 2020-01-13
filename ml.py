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
    #filenames = traverse_directory("testing_data4/" + "/lines")
    csvs = []
    for line_number, list_of_lines in filenames.items():
        for line in list_of_lines:
            data = pd.read_csv('testing_data2/lines/' + line_number + \
                                            '/' + line)
            csvs.append(data)
    df = pd.concat(csvs)
    df.to_csv("concatenated.csv", index=False)

def split_train_test(df):
    nth = 4
    training_data = np.array()
    testing_data = np.array()

    #for i, row in df.iterrows():
    #    if(i % nth == 0 and i != 0):
    #        #testing_data.append(
    #        pass
        
    #return training_data, testing_data

def count_delay_statuses(training_data):
    zeros = len(training_data.loc[training_data["delay_status"] == 0])
    ones = len(training_data.loc[training_data["delay_status"] == 1])
    twos = len(training_data.loc[training_data["delay_status"] == 2])

    print(zeros)
    print(ones)
    print(twos)

def learn(df):
    df.dropna(inplace=True)
    df.pop("time")
    df.pop("plannedLeaveTime")
    df.pop("previousStopArrivalTime")
    df.pop("previousStopLeaveTime")
    df.pop("nextStopTimetableVisitTime")

    #split_train_test(df)
    training_data, testing_data = train_test_split(df, test_size=0.3)
    
    train_labels = training_data.pop("delay_status")
    test_labels = testing_data.pop("delay_status")

    train_stats = training_data.describe().transpose()
    test_stats = testing_data.describe().transpose()

    normed_train_data = norm(training_data, train_stats)
    normed_test_data = norm(testing_data, train_stats)
    
    number_of_features = 12

    model = build_model(number_of_features)

    class_names = ["late", "early", "on time"]

    model.fit(normed_train_data, train_labels, epochs=1, verbose=1)

    test_loss, test_acc = model.evaluate(normed_test_data, test_labels)

    predictions = model.predict(normed_test_data)
    print(predictions[0])
    print(predictions[1])

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
