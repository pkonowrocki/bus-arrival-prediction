import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import seaborn as sns
import matplotlib.pyplot as plt
from utils import traverse_directory
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
import os

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

def run_neural_network(X_train, Y_train, X_test, Y_test):
    input_shape = X_train.shape[1:]
    model = build_model(input_shape)

    # Fit model to the dataset
    model.fit(X_train, Y_train, epochs=1, verbose=1)

    # Evaluate on the testing dataset
    test_loss, test_acc = model.evaluate(X_test, Y_test)

    print('\nTest accuracy:', test_acc)

def build_model(input_shape):
    model = keras.Sequential([
        layers.Dense(64, activation='relu', 
            input_shape=input_shape),
        layers.Dense(32, activation='relu'),
        layers.Dense(3, activation='softmax'),
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    return model

def run_random_forest(X_train, Y_train, X_test, Y_test):
    rf = RandomForestClassifier(n_estimators=10, random_state=0, max_depth=2)
    rf.fit(X_train, Y_train)
    print(rf.score(X_test, Y_test))

def plot_data(df: pd.DataFrame):
    sns.pairplot(df[["delay", "time", "plannedLeaveTime", "nearestStopDistance",
                     "speed", "nextStopDistance"]], diag_kind="kde")
    plt.show()
