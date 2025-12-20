import os

class Config:
    # Read Groq API key from environment. Keep empty if not set.
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    # API endpoint (leave as-is unless you need to change provider URL)
    GROK_API_URL = "https://api.x.ai/v1/chat/completions"
    MODEL_NAME = "grok-2-vision-1212"
    TEMPERATURE = 0.3
    MAX_TOKENS = 2000
    
    # Supported languages
    LANGUAGES = {
        "English": "en",
        "Hindi (हिंदी)": "hi",
        "Spanish (Español)": "es",
        "French (Français)": "fr",
        "German (Deutsch)": "de",
        "Chinese (中文)": "zh",
        "Arabic (العربية)": "ar",
        "Portuguese (Português)": "pt",
        "Russian (Русский)": "ru",
        "Japanese (日本語)": "ja"
    }