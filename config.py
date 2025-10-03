import os

class Config:
    GROK_API_KEY = os.getenv("ENTER YOUR OWN API KEY (I DIDN'T INCLUDE MINE)")
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