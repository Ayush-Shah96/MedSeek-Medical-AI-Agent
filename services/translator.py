import requests
from config import Config

def translate_result(result, target_language, api_key):
    """
    Translate analysis result to target language using Groq API
    """
    if target_language == "en":
        return result
    
    # Language names mapping
    lang_names = {
        "hi": "Hindi",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "zh": "Chinese",
        "ar": "Arabic",
        "pt": "Portuguese",
        "ru": "Russian",
        "ja": "Japanese"
    }
    
    target_lang_name = lang_names.get(target_language, "the target language")
    
    system_prompt = f"""You are a professional medical translator. Translate the following medical analysis to {target_lang_name}. 
Maintain medical accuracy and terminology. Return ONLY the translated JSON in the exact same format.

Translate these fields:
- disease
- medications (array of strings)
- preventions (array of strings)
- specialist
- notes

Keep "confidence" in English (High/Medium/Low).

Return ONLY valid JSON, no additional text."""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": f"Translate this medical analysis to {target_lang_name}:\n\n{str(result)}"
        }
    ]
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": Config.MODEL_NAME,
        "messages": messages,
        "temperature": 0.1,
        "max_tokens": Config.MAX_TOKENS
    }
    
    try:
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
            return result  # Return original if translation fails
        
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        
        # Extract JSON from response
        import json
        start_idx = content.find("{")
        end_idx = content.rfind("}") + 1
        if start_idx != -1 and end_idx != 0:
            json_str = content[start_idx:end_idx]
            translated_result = json.loads(json_str)
            return translated_result
        else:
            return result
    except:
        return result  # Return original if translation fails
