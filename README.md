# Medical AI Agent (Local)

This project provides a local, offline Medical AI Agent that accepts either text symptoms or medical images and returns a predicted disease and associated precautions.

Demo Video : https://www.loom.com/share/0f2c6acd947e42f3a36fcf1c754e37b7

Folder layout

medical-ai-agent/
 - data/ (place your datasets here)
   - symptoms/symptoms_df.csv  # CSV with `symptoms` and `disease` columns
   - images/<class_name>/*     # folders with images for transfer learning
   - precautions.csv           # mapping of Disease -> Precautions
 - models/                     # saved models after training
 - src/                        # training scripts and utilities
 - app.py                      # Streamlit UI and orchestrator

Quick start

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Prepare data:
- Put your symptom CSV at `data/symptoms/symptoms_df.csv` with columns `symptoms` and `disease`.
- Put your images in `data/images/<label>/*` directories.
- Update `data/precautions.csv` with disease -> precautions mapping.

3. Train models (optional; app will run but advise to train first):
```
python -m src.train_symptoms
python -m src.train_vision
```

4. Run the Streamlit app:
```
streamlit run app.py
```

Medical Disclaimer

This tool is for educational and demonstration purposes only and does NOT provide medical advice. Always consult a qualified healthcare professional for diagnosis or treatment.
