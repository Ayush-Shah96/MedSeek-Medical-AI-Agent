import gradio as gr
from services.symptom_analysis import analyze_symptoms
from services.image_analysis import analyze_image_with_symptoms
from services.pdf_generator import generate_pdf_report
from services.translator import translate_result
from config import Config
import os
from datetime import datetime

def process_medical_input(symptoms, image, api_key, language, patient_name, patient_age):
    """
    Process medical input and return analysis
    """
    if not symptoms and image is None:
        return (
            "⚠️ Please provide symptoms or upload an image", 
            "", "", "", "", "", "", None
        )
    
    if not api_key:
        return (
            "⚠️ Please enter your Grok API key", 
            "", "", "", "", "", "", None
        )
    
    try:
        # Get language code
        lang_code = Config.LANGUAGES.get(language, "en")
        
        # Analyze symptoms/image
        if image is not None:
            result = analyze_image_with_symptoms(symptoms, image, api_key)
        else:
            result = analyze_symptoms(symptoms, api_key)
        
        # Translate if not English
        if lang_code != "en":
            result = translate_result(result, lang_code, api_key)
        
        # Format medications and preventions
        medications_text = "\n".join([f"• {med}" for med in result.get("medications", [])])
        preventions_text = "\n".join([f"• {prev}" for prev in result.get("preventions", [])])
        
        # Generate PDF report
        pdf_path = generate_pdf_report(
            result=result,
            symptoms=symptoms,
            patient_name=patient_name,
            patient_age=patient_age,
            image_path=image,
            language=language
        )
        
        return (
            "",  # error (empty means success)
            result.get("disease", "Unknown"),
            medications_text,
            preventions_text,
            result.get("specialist", "General Physician"),
            result.get("confidence", "Medium"),
            result.get("notes", ""),
            pdf_path
        )
    
    except Exception as e:
        # FIXED: Return tuple with 8 values, not a dictionary/set
        return (
            f"❌ Error: {str(e)}", 
            "", "", "", "", "", "", None
        )

def create_interface():
    """
    Create Gradio interface
    """
    with gr.Blocks(theme=gr.themes.Soft(), title="MedSeek - AI Medical Assistant") as demo:
        gr.Markdown(
            """
            # 🏥 MedSeek - AI Medical Diagnostic Assistant
            ### Analyze symptoms and medical images using AI | Multi-Language Support | PDF Reports
            
            **Disclaimer:** This tool is for informational purposes only. Always consult a qualified healthcare professional for proper medical diagnosis and treatment.
            """
        )
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 📝 Input Information")
                
                api_key_input = gr.Textbox(
                    label="🔑 Grok API Key",
                    type="password",
                    placeholder="Enter your Grok API key (xai-...)",
                    info="Get your API key from https://console.x.ai"
                )
                
                with gr.Row():
                    patient_name_input = gr.Textbox(
                        label="👤 Patient Name (Optional)",
                        placeholder="John Doe"
                    )
                    patient_age_input = gr.Textbox(
                        label="🎂 Age (Optional)",
                        placeholder="25"
                    )
                
                language_selector = gr.Dropdown(
                    choices=list(Config.LANGUAGES.keys()),
                    value="English",
                    label="🌍 Select Language",
                    info="Results will be translated to your preferred language"
                )
                
                symptoms_input = gr.Textbox(
                    label="💬 Describe Your Symptoms",
                    placeholder="E.g., Fever, headache, sore throat for 3 days...",
                    lines=5
                )
                
                image_input = gr.Image(
                    label="📸 Upload Medical Image (Optional)",
                    type="filepath"
                )
                
                with gr.Row():
                    analyze_btn = gr.Button("🔍 Analyze", variant="primary", size="lg")
                    clear_btn = gr.ClearButton(
                        components=[symptoms_input, image_input, patient_name_input, patient_age_input],
                        value="🗑️ Clear",
                        size="lg"
                    )
            
            with gr.Column(scale=1):
                gr.Markdown("### 📊 Analysis Results")
                
                error_output = gr.Markdown(label="Status", visible=True)
                
                disease_output = gr.Textbox(
                    label="🦠 Identified Condition",
                    interactive=False
                )
                
                confidence_output = gr.Textbox(
                    label="📈 Confidence Level",
                    interactive=False
                )
                
                medications_output = gr.Textbox(
                    label="💊 Recommended Medications",
                    lines=4,
                    interactive=False
                )
                
                preventions_output = gr.Textbox(
                    label="🛡️ Preventions & Care",
                    lines=4,
                    interactive=False
                )
                
                specialist_output = gr.Textbox(
                    label="👨‍⚕️ Specialist to Consult",
                    interactive=False
                )
                
                notes_output = gr.Textbox(
                    label="📋 Additional Notes",
                    lines=3,
                    interactive=False
                )
                
                pdf_output = gr.File(
                    label="📄 Download PDF Report",
                    interactive=False
                )
        
        gr.Markdown(
            """
            ---
            ### 📌 How to Use:
            1. **Enter your Grok API Key** (required)
            2. **Select your preferred language** (optional - defaults to English)
            3. **Add patient details** (optional - for personalized PDF report)
            4. **Describe your symptoms** in detail
            5. **Upload an image** if you have visible symptoms (optional)
            6. Click **Analyze** to get AI-powered insights
            7. **Download PDF report** with complete analysis
            
            ### 🌍 Supported Languages:
            English, Hindi, Spanish, French, German, Chinese, Arabic, Portuguese, Russian, Japanese
            
            ### ⚕️ Specialists Guide:
            - **Dermatologist**: Skin conditions, rashes, acne
            - **Cardiologist**: Heart-related symptoms
            - **Orthopedic**: Bone, joint, muscle issues
            - **Dentist**: Teeth and oral health
            - **General Physician**: Common ailments, fever, infections
            
            ### 📄 PDF Report Includes:
            - Patient information
            - Symptoms analysis
            - Diagnostic findings
            - Medication recommendations
            - Prevention measures
            - Specialist recommendations
            - Timestamp and reference number
            """
        )
        
        analyze_btn.click(
            fn=process_medical_input,
            inputs=[
                symptoms_input,
                image_input,
                api_key_input,
                language_selector,
                patient_name_input,
                patient_age_input
            ],
            outputs=[
                error_output,
                disease_output,
                medications_output,
                preventions_output,
                specialist_output,
                confidence_output,
                notes_output,
                pdf_output
            ]
        )
    
    return demo

if __name__ == "__main__":
    demo = create_interface()
    demo.launch()