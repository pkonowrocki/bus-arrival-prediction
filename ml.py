import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import seaborn as sns
import matplotlib.pyplot as plt
from utils import traverse_directory
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import os

# filenames is hashmap in form of -> line (string) : list (list of strings)
def hashmap_to_single_df(path_to_traverse="testing_data4/" + "/lines"):
    filenames = traverse_directory(path_to_traverse)
    csvs = []
    for line_number, list_of_lines in filenames.items():
        for line in list_of_lines:
            data = pd.read_csv('testing_data4/lines/' + line_number + \
                                            '/' + line)
            csvs.append(data)
    df = pd.concat(csvs)
    df.to_csv("concatenated.csv", index=False, header=False)

def convert_all_csv(path_to_traverse="testing_data/" + "/lines"):
    filenames = traverse_directory(path_to_traverse)
    csvs = []

    lines_directory = "testing_data4/c_lines"
    if not os.path.exists(lines_directory):
        os.makedirs(lines_directory)

    for line_number, list_of_lines in filenames.items():
        for line in list_of_lines:
            path = "testing_data4/lines/" + line_number + "/" + line
            changed_path = "testing_data4/c_lines/" + line_number + "/" + line

            if not os.path.exists(lines_directory + "/" + line_number):
                os.makedirs(lines_directory + "/" + line_number)

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

def run_neural_network(df):
    training_data, testing_data = train_test_split(df, test_size=0.3)
    
    train_labels = training_data.pop("delay_status")
    test_labels = testing_data.pop("delay_status")

    train_stats = training_data.describe().transpose()
    test_stats = testing_data.describe().transpose()

    normed_train_data = norm(training_data, train_stats)
    normed_test_data = norm(testing_data, train_stats)
    
    number_of_features = 11

    model = build_model(number_of_features)

    model.fit(normed_train_data, train_labels, epochs=1, verbose=1)

    test_loss, test_acc = model.evaluate(normed_test_data, test_labels)

    predictions = model.predict(normed_test_data)

    print('\nTest accuracy:', test_acc)

def build_model(input_shape):
    model = keras.Sequential([
        layers.Dense(64, activation='relu', 
            input_shape=[input_shape]),
        layers.Dense(32, activation='relu'),
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
