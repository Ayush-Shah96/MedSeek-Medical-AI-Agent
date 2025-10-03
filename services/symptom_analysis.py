import requests
import json
from config import Config

def analyze_symptoms(symptoms, api_key):
    """
    Analyze text symptoms using Grok API
    """
    system_prompt = """You are an expert medical AI assistant. Analyze the provided symptoms to provide:
1. Disease Name: Identify the most likely condition
2. Medications: Recommend appropriate treatments
3. Preventions: Suggest preventive measures and care instructions
4. Specialist: Suggest the appropriate medical specialist

Provide your response in this exact JSON format:
{
  "disease": "Disease name",
  "medications": ["medication1", "medication2", "medication3"],
  "preventions": ["prevention1", "prevention2", "prevention3"],
  "specialist": "Specialist type (e.g., Dermatologist, Cardiologist, Orthopedic, Dentist, General Physician)",
  "confidence": "High/Medium/Low",
  "notes": "Additional important notes and when to seek immediate care"
}

IMPORTANT: This is for informational purposes only. Always recommend consulting a healthcare professional for proper diagnosis."""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": f"Analyze these symptoms: {symptoms}"
        }
    ]
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": Config.MODEL_NAME,
        "messages": messages,
        "temperature": Config.TEMPERATURE,
        "max_tokens": Config.MAX_TOKENS
    }
    
    response = requests.post(
        Config.GROK_API_URL,
        headers=headers,
        json=payload,
        timeout=60
    )
    
    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code} - {response.text}")
    
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    
    # Extract JSON from response
    try:
        start_idx = content.find("{")
        end_idx = content.rfind("}") + 1
        if start_idx != -1 and end_idx != 0:
            json_str = content[start_idx:end_idx]
            result = json.loads(json_str)
            return result
        else:
            raise ValueError("No JSON found in response")
    except:
        return {
            "disease": "Analysis completed - see notes",
            "medications": ["Consult healthcare provider for specific medications"],
            "preventions": ["Follow general health guidelines", "Stay hydrated", "Get adequate rest"],
            "specialist": "General Physician",
            "confidence": "Medium",
            "notes": content
        }
def analyze_image_with_symptoms(symptoms, image_path, api_key):
    """
    Analyze image along with text symptoms using Grok API
    """
    system_prompt = """You are an expert medical AI assistant. Analyze the provided symptoms and medical image to provide:
1. Disease Name: Identify the most likely condition
2. Medications: Recommend appropriate treatments
3. Preventions: Suggest preventive measures and care instructions
4. Specialist: Suggest the appropriate medical specialist           """