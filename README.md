# 🏥 MedSeek - AI Medical Diagnostic Assistant

[![MedSeek Project](https://img.shields.io/badge/MedSeek-AI%20Medical%20Assistant-blue?style=for-the-badge)](https://huggingface.co/spaces/ayush-kale-96/MedSeek)

**An AI-powered medical assistant that analyzes symptoms and medical images to provide diagnostic insights with multi-language support and professional PDF report generation.**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [API](#-api-setup) • [Deployment](#-deployment)


---

## 🌟 Features

### Core Capabilities
- 💬 **Text-based Symptom Analysis** - Describe symptoms in natural language
- 📸 **Medical Image Analysis** - Upload images of rashes, scars, wounds, and skin conditions
- 🔍 **AI-Powered Diagnosis** - Get preliminary diagnostic insights using Grok-2-Vision AI
- 💊 **Medication Recommendations** - Receive treatment suggestions
- 🛡️ **Prevention & Care** - Get preventive measures and care instructions
- 👨‍⚕️ **Specialist Recommendations** - Know which doctor to consult

### Advanced Features
- 🌍 **Multi-Language Support** - Available in 10 languages
- 📄 **Professional PDF Reports** - Generate detailed medical reports
- 🎯 **High Accuracy** - Powered by Grok-2-Vision-1212 model
- 🔒 **Privacy-Focused** - No data storage, real-time processing only
- ⚡ **Fast Processing** - Get results in seconds

---

## 🌍 Supported Languages

<table>
<tr>
<td>🇬🇧 English</td>
<td>🇮🇳 Hindi (हिंदी)</td>
<td>🇪🇸 Spanish (Español)</td>
<td>🇫🇷 French (Français)</td>
</tr>
<tr>
<td>🇩🇪 German (Deutsch)</td>
<td>🇨🇳 Chinese (中文)</td>
<td>🇸🇦 Arabic (العربية)</td>
<td>🇵🇹 Portuguese (Português)</td>
</tr>
<tr>
<td>🇷🇺 Russian (Русский)</td>
<td>🇯🇵 Japanese (日本語)</td>
<td colspan="2"></td>
</tr>
</table>

---

## 📁 Project Structure

```
MedSeek/
│
├── app.py                      # Main application entry point
├── config.py                   # Configuration and settings
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation (this file)
│
├── routes/
│   ├── __init__.py            # Package initializer
│   └── main.py                # Gradio UI interface
│
├── services/
│   ├── __init__.py            # Package initializer
│   ├── symptom_analysis.py    # Text-based symptom analysis
│   ├── image_analysis.py      # Image + symptom analysis
│   ├── translator.py          # Multi-language translation service
│   └── pdf_generator.py       # Professional PDF report generation
│
└── reports/                    # Generated PDF reports (auto-created)
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Grok API key from [xAI Console](https://console.x.ai)
 - Groq API key (set `GROQ_API_KEY` environment variable)

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/medseek.git
cd medseek
```

2. **Create virtual environment** (recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables** (optional)
```bash
# Create .env file
echo "GROQ_API_KEY=your_api_key_here" > .env
```

5. **Run the application**
```bash
# Option A: Run the original Gradio demo
python app.py

# Option B: Run the new Streamlit app
streamlit run streamlit_app.py
```

6. **Access the application**
```
If you ran the Gradio demo (Option A) open: http://localhost:7860

If you ran the Streamlit app (Option B) open: http://localhost:8501
```

---

## 🎯 Usage

### Quick Start Guide

1. **Enter API Key**
   - Get your Groq API key and set it as `GROQ_API_KEY` or enter it in the "🔑 Groq API Key" field

2. **Select Language** (Optional)
   - Choose your preferred language from the dropdown
   - Results will be translated automatically

3. **Add Patient Information** (Optional)
   - Enter patient name and age for personalized reports

4. **Describe Symptoms**
   - Be specific: Include duration, severity, and location
   - Example: "Fever (102°F) for 3 days, severe headache, sore throat"

5. **Upload Medical Image** (Optional)
   - Supported formats: JPG, PNG
   - Best for: Rashes, wounds, skin conditions, scars

6. **Analyze**
   - Click the "🔍 Analyze" button
   - Wait for AI processing (typically 5-10 seconds)

7. **Review Results**
   - View identified condition
   - Check medication recommendations
   - Read prevention measures
   - Note specialist recommendations

8. **Download PDF Report**
   - Click the download button for the PDF
   - Share with your healthcare provider

## 📊 Features Breakdown

### PDF Report Contents

Generated reports include:
- ✅ Patient Information (name, age)
- ✅ Report ID and timestamp
- ✅ Reported symptoms (detailed)
- ✅ Medical images (if provided)
- ✅ AI diagnostic analysis
- ✅ Confidence level assessment
- ✅ Medication recommendations
- ✅ Prevention and care instructions
- ✅ Specialist recommendations
- ✅ Additional medical notes
- ✅ Professional disclaimer

### Specialist Categories

| Specialist | Conditions Treated |
|-----------|-------------------|
| 🫀 **Cardiologist** | Heart conditions, chest pain, palpitations |
| 🦴 **Orthopedic** | Bone fractures, joint pain, muscle injuries |
| 🧠 **Neurologist** | Headaches, seizures, neurological issues |
| 👁️ **Ophthalmologist** | Eye problems, vision issues |
| 🦷 **Dentist** | Tooth pain, oral health issues |
| 🩺 **Dermatologist** | Skin conditions, rashes, acne |
| 🫁 **Pulmonologist** | Respiratory issues, breathing problems |
| 🏥 **General Physician** | Common ailments, fever, infections |

---

## 🔒 Privacy & Security

- ✅ **No Data Storage**: All processing happens in real-time
- ✅ **Secure API**: All API calls use HTTPS encryption
- ✅ **Local PDF Generation**: Reports generated locally, not stored on servers
- ✅ **No Tracking**: No user analytics or tracking
- ✅ **API Key Protection**: Keys are never logged or stored

---

## ⚠️ Medical Disclaimer

**IMPORTANT**: This tool is for **informational and educational purposes only**.

- ❌ **NOT a replacement** for professional medical advice
- ❌ **NOT for emergencies** - Call emergency services for urgent issues
- ❌ **NOT a diagnostic tool** - Always consult qualified healthcare professionals
- ✅ Use as a **preliminary screening** tool only
- ✅ Always **verify with doctors** before taking any action
- ✅ In case of serious symptoms, **seek immediate medical attention**

---

## 🛠️ Technical Details

### Technology Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | Gradio 4.44.0 |
| **AI Model** | Grok-2-Vision-1212 (xAI) |
| **Backend** | Python 3.8+ |
| **PDF Generation** | ReportLab 4.0.7 |
| **Image Processing** | Pillow 10.2.0 |
| **HTTP Client** | Requests 2.31.0 |

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 MedSeek

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

v>
