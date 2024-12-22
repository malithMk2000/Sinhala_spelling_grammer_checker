import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

def create_model(vocab_size, embedding_dim=128, lstm_units=128):
    model = Sequential([
        Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=None),
        LSTM(units=lstm_units, return_sequences=False),
        Dense(units=vocab_size, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model
