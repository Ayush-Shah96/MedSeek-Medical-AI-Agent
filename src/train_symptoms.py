"""Train a RandomForest classifier on symptom->disease CSV data.

Expected CSV format: `symptoms` column (text) and `disease` column (label).
Place your dataset at `data/symptoms/symptoms_df.csv`.
"""
import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / 'data'
MODELS_DIR = ROOT / 'models'
MODELS_DIR.mkdir(parents=True, exist_ok=True)


def train_from_training_csv(path: Path, save=True):
    df = pd.read_csv(path)
    if 'prognosis' not in df.columns:
        raise ValueError('Training.csv must contain a `prognosis` column')
    # features are all columns except prognosis
    feature_cols = [c for c in df.columns if c != 'prognosis']
    X = df[feature_cols].fillna(0)
    # ensure numeric
    X = X.astype(int)
    y = df['prognosis']

    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    X_train, X_val, y_train, y_val = train_test_split(X, y_enc, test_size=0.2, random_state=42, stratify=y_enc)

    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    clf.fit(X_train, y_train)

    preds = clf.predict(X_val)
    print('Validation classification report:')
    print(classification_report(y_val, preds, target_names=le.classes_))

    if save:
        joblib.dump(clf, MODELS_DIR / 'symptom_model.pkl')
        # save label encoder and feature names
        joblib.dump(le, MODELS_DIR / 'label_encoder.pkl')
        with open(MODELS_DIR / 'symptom_features.json', 'w') as f:
            json.dump(feature_cols, f)
        print('Saved symptom model, label encoder and feature list to models/')


def train_from_text_csv(path: Path, save=True):
    df = pd.read_csv(path)
    if 'symptoms' not in df.columns or 'disease' not in df.columns:
        raise ValueError('CSV must contain `symptoms` and `disease` columns')
    X_text = df['symptoms'].fillna('')
    y = df['disease']

    vect = TfidfVectorizer(max_features=2000, stop_words='english')
    X = vect.fit_transform(X_text)

    le = LabelEncoder()
    y_enc = le.fit_transform(y)

    X_train, X_val, y_train, y_val = train_test_split(X, y_enc, test_size=0.2, random_state=42, stratify=y_enc)

    clf = RandomForestClassifier(n_estimators=200, random_state=42)
    clf.fit(X_train, y_train)

    preds = clf.predict(X_val)
    print('Validation classification report:')
    print(classification_report(y_val, preds, target_names=le.classes_))

    if save:
        joblib.dump(clf, MODELS_DIR / 'symptom_model.pkl')
        joblib.dump(vect, MODELS_DIR / 'vectorizer.pkl')
        joblib.dump(le, MODELS_DIR / 'label_encoder.pkl')
        print('Saved symptom model, vectorizer and label encoder to models/')


def train(save=True):
    # detect available datasets
    training_csv = DATA_ROOT / 'Training.csv'
    text_csv = DATA_ROOT / 'symptoms' / 'symptoms_df.csv'
    generic_csv = DATA_ROOT / 'Disease_symptom_and_patient_profile_dataset.csv'

    if training_csv.exists():
        print('Found Training.csv — training from binary feature table')
        train_from_training_csv(training_csv, save=save)
    elif text_csv.exists():
        print('Found symptoms_df.csv — training from text->disease mapping')
        train_from_text_csv(text_csv, save=save)
    elif generic_csv.exists():
        print('Found Disease_symptom_and_patient_profile_dataset.csv — attempting to use Disease and simple feature cols')
        # naive handling: attempt to use basic symptom columns (Y/N -> 1/0)
        df = pd.read_csv(generic_csv)
        # try to infer which columns are symptoms by dtype
        possible_symptoms = [c for c in df.columns if c.lower() not in ('disease','age','gender','outcome variable','blood pressure','cholesterol level')]
        df_sym = df[possible_symptoms].applymap(lambda v: 1 if str(v).strip().lower() in ('yes','true','1') else 0)
        df_sym['prognosis'] = df['Disease']
        tmp_path = DATA_ROOT / 'Training_from_generic.csv'
        df_sym.to_csv(tmp_path, index=False)
        train_from_training_csv(tmp_path, save=save)
    else:
        raise FileNotFoundError('No suitable symptom dataset found in data/ (looked for Training.csv or data/symptoms/symptoms_df.csv)')


if __name__ == '__main__':
    train()
