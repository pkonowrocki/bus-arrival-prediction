import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MaxNLocator

def plot_data(df):
    sns.pairplot(df[["delay", "time", "plannedLeaveTime", "nearestStopDistance",
                     "speed", "nextStopDistance"]], diag_kind="kde")
    plt.show()

def plot_predictions(predictions, Y_test):
    pass

def plot_training_process(history):
    plt.plot(history.history['loss'], label='train dataset')
    plt.plot(history.history['val_loss'], label='validation dataset')
    plt.ylabel("Loss")
    plt.xlabel("Number of epochs")
    plt.title("Training process")
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.legend()
    plt.show()
