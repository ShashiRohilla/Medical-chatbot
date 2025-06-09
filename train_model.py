import json
import numpy as np
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv1D, GlobalMaxPooling1D, Embedding
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

# Load data
with open("chat_data.json") as f:
    data = json.load(f)

# Prepare texts and labels
texts = []
labels = []
responses = {}

for item in data:
    for pattern in item["patterns"]:
        texts.append(pattern)
        labels.append(item["intent"])
    responses[item["intent"]] = item["response"]

# Tokenize texts
tokenizer = Tokenizer()
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)
max_len = max(len(x) for x in sequences)
X = pad_sequences(sequences, maxlen=max_len)

# Encode labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(labels)

# Save tokenizer and label encoder
with open("tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer, f)

with open("label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

# Build CNN model
vocab_size = len(tokenizer.word_index) + 1
model = Sequential([
    Embedding(vocab_size, 128, input_length=max_len),
    Conv1D(64, 5, activation="relu"),
    GlobalMaxPooling1D(),
    Dense(64, activation="relu"),
    Dense(len(set(y)), activation="softmax")
])

model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
model.fit(X, y, epochs=10, verbose=1)

model.save("chat_model.keras")
print("✅ Model trained and saved!")
