import numpy as np
import tensorflow as tf

def train_model():
    # Sample XOR dataset
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([[0], [1], [1], [0]])

    # Define a simple neural network using Keras (from TensorFlow)
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(8, input_dim=2, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    # Compile the model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Train the model
    model.fit(X, y, epochs=500, batch_size=4, verbose=0)
    
    return model

def predict_output(model):
    # Test predictions
    X_test = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    predictions = model.predict(X_test)
    output_to_send = predictions.tolist()
    return output_to_send
