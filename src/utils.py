import os
import pandas as pd
import numpy as np
from PIL import Image

from sklearn.feature_extraction.text import TfidfVectorizer

import tensorflow as tf


def load_precautions(csv_path):
    if not os.path.exists(csv_path):
        return {}
    df = pd.read_csv(csv_path)
    # normalize keys to allow case/whitespace-insensitive lookup
    mapping = {}
    for _, row in df.iterrows():
        k = str(row['Disease']).strip().lower()
        mapping[k] = str(row['Precautions'])
    return mapping


def preprocess_texts(texts, vectorizer: TfidfVectorizer = None):
    if vectorizer is None:
        vectorizer = TfidfVectorizer(max_features=2000, stop_words='english')
        X = vectorizer.fit_transform(texts)
        return X, vectorizer
    else:
        X = vectorizer.transform(texts)
        return X, vectorizer


def load_and_preprocess_image(img, target_size=(224, 224)):
    if isinstance(img, (str, os.PathLike)):
        img = Image.open(img).convert('RGB')
    elif isinstance(img, Image.Image):
        img = img.convert('RGB')
    else:
        # assume file-like
        img = Image.open(img).convert('RGB')

    img = img.resize(target_size)
    arr = np.array(img).astype('float32') / 255.0
    arr = np.expand_dims(arr, 0)
    return arr


def build_vision_model(num_classes):
    base = tf.keras.applications.ResNet50(weights='imagenet', include_top=False, input_shape=(224,224,3))
    base.trainable = False
    x = tf.keras.layers.GlobalAveragePooling2D()(base.output)
    x = tf.keras.layers.Dense(256, activation='relu')(x)
    x = tf.keras.layers.Dropout(0.3)(x)
    outputs = tf.keras.layers.Dense(num_classes, activation='softmax')(x)
    model = tf.keras.Model(inputs=base.input, outputs=outputs)
    return model


def text_to_feature_vector(symptoms_text: str, feature_names):
    """Convert a free-text symptoms string into a binary vector aligned to feature_names.

    It matches feature names (underscores allowed) against tokens in the input.
    """
    text = symptoms_text.lower()
    # simple tokenization
    tokens = set([t.strip().replace('-', '_') for t in __import__('re').split(r"\W+", text) if t])
    vec = []
    for fn in feature_names:
        # feature names in dataset often contain underscores; match by token parts
        parts = fn.lower().split('_')
        match = any(p in tokens for p in parts) or fn.lower() in tokens
        vec.append(1 if match else 0)
    import numpy as np
    return np.array(vec).reshape(1, -1)
