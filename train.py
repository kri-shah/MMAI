import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import joblib

def load_data(file_path):
    return pd.read_csv(file_path)

def preprocess_data(data):
    data = data.sample(frac=1, random_state=42) 
    X = data.drop(['wl', 'fighterx', 'fightery', 'stanceopenstancex','stanceorthodoxx','stancesouthpawx',
                   'stanceswitchx', 'stanceopenstancey','stanceorthodoxy','stancesouthpawy','stanceswitchy'], axis=1)
    y = data['wl'].astype('float32')
    return X, y

def split_data(X, y, test_size=0.33, random_state=101):
    return train_test_split(X, y, test_size=test_size, random_state=random_state)

def normalize_data(X_train, X_test):
    scaler = MinMaxScaler()
    
    # Fit the scaler on the training data and transform both training and testing data
    X_train_normalized = scaler.fit_transform(X_train)
    X_test_normalized = scaler.transform(X_test)
    
    # Save the scaler
    joblib.dump(scaler, 'scaler.pkl')
    
    return X_train_normalized, X_test_normalized

def build_model(input_shape):
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=input_shape),  # Input layer
        tf.keras.layers.Dense(73, activation='relu'),  # Hidden layer
        tf.keras.layers.Dense(73, activation='relu'),  # Hidden layer
        tf.keras.layers.Dense(73, activation='relu'),  # Hidden layer
        tf.keras.layers.Dense(1, activation='sigmoid')  # Output layer
    ])
    return model

def train_model(model, X_train, y_train, epochs=20):
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=epochs)
    return model

def save_model(model, file_path):
    tf.keras.saving.save_model(model, file_path, overwrite=True, save_format=None)

def evaluate_model(model, X_test, y_test):
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Accuracy: {accuracy * 100:.2f}%")

if __name__ == "__main__":
    # Load data
    UFC_data = load_data('full_ufc_data.csv')

    # Preprocess data
    X, y = preprocess_data(UFC_data)

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = split_data(X, y)

    # Normalize features
    X_train_normalized, X_test_normalized = normalize_data(X_train, X_test)

    # Build the model
    model = build_model(X_train_normalized.shape[1])

    # Train the model
    trained_model = train_model(model, X_train_normalized, y_train)

    # Save the model
    save_model(trained_model, 'UFC')

    # Evaluate the model
    evaluate_model(trained_model, X_test_normalized, y_test)

