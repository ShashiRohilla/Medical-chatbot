from tensorflow.keras.models import Model
from tensorflow.keras.layers import Flatten, Dense, Dropout
from tensorflow.keras.applications import MobileNetV2
import numpy as np

# Use MobileNetV2 as base
base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights=None)

x = base_model.output
x = Flatten()(x)
x = Dense(64, activation='relu')(x)
x = Dropout(0.3)(x)
predictions = Dense(3, activation='softmax')(x)  # 3 classes: acne, eczema, normal

model = Model(inputs=base_model.input, outputs=predictions)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Simulate random weights (for demo)
# ✅ NEW (correct)
for layer in model.layers:
    weights = layer.get_weights()
    if weights:
        new_weights = [np.random.randn(*w.shape) * 0.05 for w in weights]
        layer.set_weights(new_weights)

# Save model
model.save("skin_disease_model.h5")
print("✅ Model saved as skin_disease_model.h5")
