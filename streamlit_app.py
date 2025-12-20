import streamlit as st
import tempfile
import os
from services.symptom_analysis import analyze_symptoms, analyze_image_with_symptoms
from services.translator import translate_result
from services.pdf_generator import generate_pdf_report
from config import Config


def save_uploaded_image(uploaded_file):
    if uploaded_file is None:
        return None
    suffix = os.path.splitext(uploaded_file.name)[1]
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(uploaded_file.getbuffer())
    tmp.flush()
    tmp.close()
    return tmp.name


def process_input(symptoms, image_path, api_key, language, patient_name, patient_age):
    if not symptoms and image_path is None:
        st.error("Please provide symptoms or upload an image")
        return None
    # Allow using environment variable `GROQ_API_KEY` if field left empty
    api_key = api_key or Config.GROQ_API_KEY
    if not api_key:
        st.error("Please enter your Groq API key")
        return None
        return None

    lang_code = Config.LANGUAGES.get(language, "en")

    if image_path is not None:
        result = analyze_image_with_symptoms(symptoms, image_path, api_key)
    else:
        result = analyze_symptoms(symptoms, api_key)

    if lang_code != "en":
        try:
            result = translate_result(result, lang_code, api_key)
        except Exception:
            pass

    return result


def main():
    st.set_page_config(page_title="MedSeek - AI Medical Assistant", layout="wide")
    st.title("🏥 MedSeek - AI Medical Diagnostic Assistant")

    st.sidebar.header("Input Settings")
    api_key = st.sidebar.text_input("Groq API Key", type="password", placeholder="Enter your Groq API key")
    language = st.sidebar.selectbox("Select Language", list(Config.LANGUAGES.keys()), index=0)
    patient_name = st.sidebar.text_input("Patient Name (optional)")
    patient_age = st.sidebar.text_input("Age (optional)")

    st.sidebar.markdown("---")
    st.sidebar.markdown("Disclaimer: For informational purposes only. Consult a healthcare professional.")

    with st.form(key="analysis_form"):
        symptoms = st.text_area("Describe Your Symptoms", height=150, placeholder="E.g., Fever, headache, sore throat for 3 days...")
        uploaded_image = st.file_uploader("Upload Medical Image (optional)", type=["jpg", "jpeg", "png"])
        submit = st.form_submit_button("Analyze")

    image_path = None
    if uploaded_image is not None:
        image_path = save_uploaded_image(uploaded_image)
        st.image(uploaded_image, caption="Uploaded image", use_column_width=False)

    if submit:
        with st.spinner("Analyzing..."):
            try:
                result = process_input(symptoms, image_path, api_key, language, patient_name, patient_age)
            except Exception as e:
                msg = str(e)
                if "403" in msg or "credits" in msg or "licenses" in msg or "Forbidden" in msg:
                    st.error("API access denied: your team may not have no credits or licenses. Visit your provider console to manage billing or add credits.")
                else:
                    st.error(f"Error during analysis: {e}")
                result = None

        if result:
            st.subheader("📊 Analysis Results")
            col1, col2 = st.columns([1, 1])
            with col1:
                st.text_input("Identified Condition", value=result.get("disease", "Unknown"), disabled=True)
                st.text_input("Confidence Level", value=result.get("confidence", "Medium"), disabled=True)
                st.text_input("Specialist to Consult", value=result.get("specialist", "General Physician"), disabled=True)

            with col2:
                meds = result.get("medications", [])
                prevs = result.get("preventions", [])
                st.text_area("Recommended Medications", value="\n".join([f"• {m}" for m in meds]), height=120, disabled=True)
                st.text_area("Preventions & Care", value="\n".join([f"• {p}" for p in prevs]), height=120, disabled=True)

            if result.get("notes"):
                st.markdown("**Additional Notes**")
                st.write(result.get("notes"))

            try:
                pdf_path = generate_pdf_report(
                    result=result,
                    symptoms=symptoms,
                    patient_name=patient_name,
                    patient_age=patient_age,
                    image_path=image_path,
                    language=language
                )
                if pdf_path and os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as f:
                        pdf_bytes = f.read()
                    st.download_button("📄 Download PDF Report", data=pdf_bytes, file_name=os.path.basename(pdf_path), mime="application/pdf")
            except Exception as e:
                st.warning(f"Could not generate PDF: {e}")

    # Cleanup temporary file(s) if any
    if uploaded_image is None and 'image_path' in locals() and image_path and os.path.exists(image_path):
        try:
            os.remove(image_path)
        except Exception:
            pass


if __name__ == "__main__":
    main()
