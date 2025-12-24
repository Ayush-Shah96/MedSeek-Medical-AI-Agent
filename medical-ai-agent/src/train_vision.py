"""Train a vision classifier using transfer learning (ResNet50).

Place images in `data/images/<class_name>/*` folders.
"""
import os
from pathlib import Path
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.preprocessing import image_dataset_from_directory
from src.utils import build_vision_model

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / 'data' / 'images'
MODELS_DIR = ROOT / 'models'
MODELS_DIR.mkdir(parents=True, exist_ok=True)


def train(batch_size=16, epochs=3):
    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Image directory not found at {DATA_DIR}. Place your images there.")

    train_ds = image_dataset_from_directory(
        DATA_DIR,
        labels='inferred',
        label_mode='categorical',
        batch_size=batch_size,
        image_size=(224,224),
        validation_split=0.2,
        subset='training',
        seed=42
    )

    val_ds = image_dataset_from_directory(
        DATA_DIR,
        labels='inferred',
        label_mode='categorical',
        batch_size=batch_size,
        image_size=(224,224),
        validation_split=0.2,
        subset='validation',
        seed=42
    )

    class_names = train_ds.class_names
    num_classes = len(class_names)
    model = build_vision_model(num_classes)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # small training loop; users should tune and increase epochs
    model.fit(train_ds, validation_data=val_ds, epochs=epochs)

    model.save(MODELS_DIR / 'vision_model.h5')
    # save class names
    with open(MODELS_DIR / 'vision_classes.txt', 'w') as f:
        f.write('\n'.join(class_names))
    print('Saved vision model and classes to models/')


if __name__ == '__main__':
    train()
