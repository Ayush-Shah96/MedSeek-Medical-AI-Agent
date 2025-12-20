import requests
import json
import base64
from config import Config

def encode_image(image_path):
    """
    Encode image to base64
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image_with_symptoms(symptoms, image_path, api_key):
    """
    Analyze image with optional symptoms using Grok Vision API
    """
    system_prompt = """You are an expert medical AI assistant with vision capabilities. Analyze the provided medical image and symptoms to provide:
1. Disease Name: Identify the most likely condition based on visual and textual information
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
  "notes": "Additional important notes including visual observations and when to seek immediate care"
}

IMPORTANT: This is for informational purposes only. Always recommend consulting a healthcare professional for proper diagnosis."""

    base64_image = encode_image(image_path)
    
    user_content = []
    
    if symptoms:
        user_content.append({
            "type": "text",
            "text": f"Analyze this medical image along with these symptoms: {symptoms}"
        })
    else:
        user_content.append({
            "type": "text",
            "text": "Analyze this medical image and identify any conditions visible."
        })
    
    user_content.append({
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
        }
    })
    
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_content
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

    # Handle permission / billing errors with clearer message
    if response.status_code == 403:
        try:
            err = response.json()
            err_msg = err.get("error") or err.get("message") or response.text
        except Exception:
            err_msg = response.text
        raise Exception(f"API 403 Forbidden: {err_msg}. Your team may not have credits or licenses. Visit https://console.x.ai to manage billing.")

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
            "preventions": ["Follow general health guidelines", "Keep area clean", "Avoid irritation"],
            "specialist": "Dermatologist or General Physician",
            "confidence": "Medium",
            "notes": content
        }
    