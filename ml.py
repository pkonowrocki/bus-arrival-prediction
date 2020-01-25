import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans

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
    print("Random forest classifier is fitting data")
    rf.fit(X_train, Y_train)
    print("Random forest classifier score: ", rf.score(X_test, Y_test))

def run_k_means(X_train, Y_train, X_test, Y_test):
    k_means = KMeans(n_clusters=10, random_state=0)
    print("KMeans is fitting data")
    k_means.fit(X_train, Y_train)
    print("KMeans score: ", k_means.score(X_test, Y_test))
