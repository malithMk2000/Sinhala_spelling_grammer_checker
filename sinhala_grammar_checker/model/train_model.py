import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from grammar_model import create_model

# Load the dataset
data = pd.read_csv('P:/Windows/Desktop/AI/sinhala_grammar_checker/data/sinhala_grammar_dataset.csv')
sentences = data['sentence']
labels = data['label']  # Assuming binary: 0=correct, 1=incorrect

# Tokenize text
tokenizer = Tokenizer()
tokenizer.fit_on_texts(sentences)
vocab_size = len(tokenizer.word_index) + 1

# Prepare data
X = tokenizer.texts_to_sequences(sentences)
y = to_categorical(labels, num_classes=2)
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Pad sequences
from tensorflow.keras.preprocessing.sequence import pad_sequences
X_train = pad_sequences(X_train, padding='post')
X_val = pad_sequences(X_val, padding='post')

# Create and train model
model = create_model(vocab_size)
model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=5, batch_size=32)

# Save model
model.save('P:/Windows/Desktop/AI/sinhala_grammar_checker/model/model_weights.h5')
