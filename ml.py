import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from keras.callbacks import ModelCheckpoint, EarlyStopping
from sklearn import tree
import matplotlib.pyplot as plt
from plotting_functions import plot_validation_curve_decision_tree

def run_neural_network(X_train, Y_train, X_test, Y_test):
    input_shape = X_train.shape[1:]
    model = build_model(input_shape)

    # Early stopping
    es = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=5)

    # Fit model to the dataset
    history = model.fit(X_train, Y_train, epochs=40, verbose=1, validation_split=0.2, callbacks=[es])

    # Evaluate on the testing dataset
    test_loss, test_acc = model.evaluate(X_test, Y_test)

    print('\nTest accuracy:', test_acc)

    predictions = model.predict(X_test)

    return predictions, history

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
    rf = RandomForestClassifier(n_estimators=10, random_state=0, max_depth=1)
    print("Random forest classifier is fitting data")
    rfc = rf.fit(X_train, Y_train)
    #plot_validation_curve(rf, X_train, Y_train)
    print("Random forest classifier score: ", rfc.score(X_test, Y_test))

def run_k_neighbors(X_train, Y_train, X_test, Y_test):
    k_neighbors = KNeighborsClassifier(n_neighbors=3)
    print("KNeighbors is fitting data")
    k_neighbors.fit(X_train, Y_train)
    print("KNeighbors score: ", k_neighbors.score(X_test, Y_test))

def run_decision_tree(X_train, Y_train, X_test, Y_test):
    decision_tree = DecisionTreeClassifier(max_depth=1)
    plot_validation_curve_decision_tree(decision_tree, X_train, Y_train)
    print("Decision tree is fitting data")
    clf = decision_tree.fit(X_train, Y_train)
    #tree.plot_tree(clf)
    #plt.show()
    print("Decision tree score: ", clf.score(X_test, Y_test))
