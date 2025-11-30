# ===== train.py =====
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import os

# Paths
base_dir = os.path.join(os.getcwd(), "data")

# Check dataset folders
print("✅ Dataset folders found:", os.listdir(base_dir))

# Image Data Generator (with augmentation)
datagen = ImageDataGenerator(
    rescale=1.0/255,
    validation_split=0.2,  # 80% train, 20% validation
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True
)

# Training and validation sets
train_gen = datagen.flow_from_directory(
    base_dir,
    target_size=(128, 128),
    batch_size=32,
    class_mode='categorical',
    subset='training'
)

val_gen = datagen.flow_from_directory(
    base_dir,
    target_size=(128, 128),
    batch_size=32,
    class_mode='categorical',
    subset='validation'
)

# Class names
print("🔖 Class labels:", train_gen.class_indices)

# CNN Model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
    MaxPooling2D(2, 2),

    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),

    Conv2D(128, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),

    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(len(train_gen.class_indices), activation='softmax')
])

# Compile Model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train Model
print("🚀 Training started...")
history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=10,
    verbose=1
)

# Save model
model_save_path = os.path.join("static", "model")
os.makedirs(model_save_path, exist_ok=True)
model.save(os.path.join(model_save_path, "mushroom_model.h5"))

print("💾 Model saved successfully at:", os.path.join(model_save_path, "mushroom_model.h5"))

# Evaluate
loss, acc = model.evaluate(val_gen, verbose=0)
print(f"✅ Final Accuracy: {acc * 100:.2f}%")
