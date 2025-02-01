from deep_translator import GoogleTranslator

# Define supported languages
LANGUAGES = {
    "English": "en",
    "Malayalam": "ml",
    "Hindi": "hi"
}

def translate_text(text, lang):
    """Translate text to the selected language"""
    if lang in LANGUAGES:
        translated = GoogleTranslator(source="auto", target=LANGUAGES[lang]).translate(text)
        return translated
    return text  # Default to English if not found

# Example usage
if __name__ == "__main__":
    print(translate_text("Hello, welcome!", "Malayalam"))  # Malayalam translation
