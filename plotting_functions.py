import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def plot_data(df):
    sns.pairplot(df[["delay", "time", "plannedLeaveTime", "nearestStopDistance",
                     "speed", "nextStopDistance"]], diag_kind="kde")
    plt.show()

def plot_predictions(predictions, Y_test):
    predicted = [np.argmax(prediction) for prediction in predictions]
    #fig, axs = plt.subplots(ncols=2)
    #sns.countplot(x=Y_test, palette="muted", ax=axs[0])
    #sns.countplot(x=predicted, palette="muted", ax=axs[1])
    #axs[1].set_xlabel("Classes")
    #sns.catplot(x=predicted, y=Y_test, kind="bar")
    plt.show()

