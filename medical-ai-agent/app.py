import streamlit as st
import os
from pathlib import Path
import joblib
import pandas as pd
from PIL import Image
import numpy as np
import tensorflow as tf

from src.utils import load_and_preprocess_image, load_precautions, text_to_feature_vector

ROOT = Path(__file__).resolve().parent
MODELS_DIR = ROOT / 'models'
DATA_DIR = ROOT / 'data'


class MedicalAgent:
    def __init__(self, models_dir=MODELS_DIR, data_dir=DATA_DIR):
        self.models_dir = Path(models_dir)
        self.data_dir = Path(data_dir)
        self.precautions = load_precautions(self.data_dir / 'precautions.csv')

        # Try to load symptom model and vectorizer
        self.symptom_model = None
        self.vectorizer = None
        self.label_encoder = None
        self.symptom_features = None
        try:
            self.symptom_model = joblib.load(self.models_dir / 'symptom_model.pkl')
            # optional vectorizer for free-text models
            try:
                self.vectorizer = joblib.load(self.models_dir / 'vectorizer.pkl')
            except Exception:
                self.vectorizer = None
            try:
                self.label_encoder = joblib.load(self.models_dir / 'label_encoder.pkl')
            except Exception:
                self.label_encoder = None
            # symptom features list (for Training.csv style datasets)
            feat_path = self.models_dir / 'symptom_features.json'
            if feat_path.exists():
                import json
                with open(feat_path) as f:
                    self.symptom_features = json.load(f)
        except Exception:
            pass

        # Try to load vision model
        self.vision_model = None
        self.vision_classes = []
        try:
            self.vision_model = tf.keras.models.load_model(self.models_dir / 'vision_model.h5')
            classes_path = self.models_dir / 'vision_classes.txt'
            if classes_path.exists():
                with open(classes_path) as f:
                    self.vision_classes = [l.strip() for l in f if l.strip()]
        except Exception:
            pass

    def predict_text(self, symptoms_text: str):
        if not self.symptom_model:
            return {'error': 'Symptom model not found. Run training.'}

        # If we have a vectorizer (text->model), use it
        if self.vectorizer is not None and self.label_encoder is not None:
            X = self.vectorizer.transform([symptoms_text])
            pred_enc = self.symptom_model.predict(X)[0]
            pred = self.label_encoder.inverse_transform([pred_enc])[0]
            precautions = self.precautions.get(pred.strip().lower(), 'No precautions available for this disease.')
            return {'disease': pred, 'precautions': precautions}

        # Otherwise, if we have symptom_features, attempt to map text into binary feature vector
        if self.symptom_features is not None and self.label_encoder is not None:
            X = text_to_feature_vector(symptoms_text, self.symptom_features)
            pred_enc = self.symptom_model.predict(X)[0]
            pred = self.label_encoder.inverse_transform([pred_enc])[0]
            precautions = self.precautions.get(pred.strip().lower(), 'No precautions available for this disease.')
            return {'disease': pred, 'precautions': precautions}

        # last resort: if label_encoder absent, try direct predict (model may output strings)
        try:
            pred = self.symptom_model.predict([symptoms_text])[0]
            precautions = self.precautions.get(pred, 'No precautions available for this disease.')
            return {'disease': pred, 'precautions': precautions}
        except Exception:
            return {'error': 'Unable to predict from text: missing vectorizer/feature mapping/label encoder. Run training.'}

    def predict_image(self, img):
        if self.vision_model is None or not self.vision_classes:
            return {'error': 'Vision model not found. Run vision training.'}
        arr = load_and_preprocess_image(img)
        preds = self.vision_model.predict(arr)
        idx = int(np.argmax(preds, axis=1)[0])
        label = self.vision_classes[idx]
        precautions = self.precautions.get(label.strip().lower(), 'No precautions available for this disease.')
        return {'disease': label, 'precautions': precautions, 'confidence': float(np.max(preds))}

    def predict_from_features(self, selected_features: list):
        """Predict given a list of selected symptom feature names."""
        if not self.symptom_model or not self.label_encoder or not self.symptom_features:
            return {'error': 'Symptom model or feature mapping not available. Run training.'}
        import numpy as _np
        feats = [1 if f in selected_features else 0 for f in self.symptom_features]
        X = _np.array(feats).reshape(1, -1)
        pred_enc = self.symptom_model.predict(X)[0]
        pred = self.label_encoder.inverse_transform([pred_enc])[0]
        precautions = self.precautions.get(pred.strip().lower(), 'No precautions available for this disease.')
        return {'disease': pred, 'precautions': precautions}


def main():
    st.set_page_config(page_title='Medical AI Agent', layout='centered')
    st.title('Medical AI Agent (Local)')

    st.markdown('**Medical Disclaimer:** This tool is for educational/demo purposes only and is NOT medical advice. Seek professional care for diagnosis and treatment.')

    agent = MedicalAgent()

    mode = st.radio('Input Type', ['Text (Symptoms)', 'Image (Upload)'])

    if mode.startswith('Text'):
        if agent.symptom_features is None:
            st.warning('No symptom feature list found. Run training to enable selection UI.')
        else:
            if 'selected_symptoms' not in st.session_state:
                st.session_state['selected_symptoms'] = []

            selected = st.multiselect('Select symptoms you are experiencing', options=agent.symptom_features, key='selected_symptoms')

            col1, col2 = st.columns([1,1])
            with col1:
                if st.button('Predict from selected symptoms'):
                    if not st.session_state['selected_symptoms']:
                        st.warning('Please select at least one symptom')
                    else:
                        res = agent.predict_from_features(st.session_state['selected_symptoms'])
                        if 'error' in res:
                            st.error(res['error'])
                        else:
                            st.success(f"Predicted disease: {res['disease']}")
                            st.info(f"Precautions: {res['precautions']}")
            def _clear_selection():
                st.session_state['selected_symptoms'] = []

            with col2:
                st.button('Clear selection', on_click=_clear_selection, key='clear_selection_btn')

    else:
        uploaded = st.file_uploader('Upload an image (e.g., skin lesion, X-ray)', type=['png','jpg','jpeg'])
        if uploaded is not None:
            st.image(uploaded, caption='Uploaded image', use_column_width=True)
            if st.button('Predict from image'):
                res = agent.predict_image(uploaded)
                if 'error' in res:
                    st.error(res['error'])
                else:
                    st.success(f"Predicted disease: {res['disease']} (confidence: {res.get('confidence', 0):.2f})")
                    st.info(f"Precautions: {res['precautions']}")


if __name__ == '__main__':
    main()
