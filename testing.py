import streamlit as st
from langdetect import detect
from googletrans import Translator
import datetime
from PIL import Image

# ✅ Set page config at the very beginning
st.set_page_config(page_title="CropGuard", page_icon="🌾")

# Import necessary modules
from weather_api import get_weather
from price_api import get_crop_price
from chatbot import get_chat_response
from suggestions import get_optimization_tips
from disease_model import detect_disease  # ✅ Gemini API integration

# Initialize Translator
translator = Translator()

# 🌍 Language Selection
language_options = {"English": "en", "Hindi": "hi", "Malayalam": "ml"}
selected_lang = st.sidebar.radio("🌐 Choose Language:", list(language_options.keys()))
lang_code = language_options[selected_lang]

# 🔤 Translation Helper
def translate_text(text, target_lang):
    if target_lang == "en":
        return text
    translation = translator.translate(text, dest=target_lang)
    return translation.text

# Crop name mappings for translation
crop_name_mapping_ml = {
    "ഉരുളക്കിഴങ്ങ്": "potato",
    "തക്കാളി": "tomato",
    "അല്ലി": "ginger",
    "അരി": "rice",
    "ഗോതമ്പ്": "wheat",
    "മുതിര": "carrot",
    "ചേരി": "beetroot",
    "മാവ്": "maize",
}

crop_name_mapping_hi = {
    "आलू": "potato",
    "टमाटर": "tomato",
    "अदरक": "ginger",
    "चावल": "rice",
    "गेंहू": "wheat",
    "गाजर": "carrot",
    "चुकंदर": "beetroot",
    "मक्का": "maize",
}

# UI Elements with Language Support
menu_items = {
    "Disease Detection": translate_text("Disease Detection", lang_code),
    "Weather Alerts": translate_text("Weather Alerts", lang_code),
    "Crop Prices": translate_text("Crop Prices", lang_code),
    "Community Chatbot": translate_text("Community Chatbot", lang_code),
    "Resource Optimization": translate_text("Resource Optimization", lang_code)
}

st.title("🌾 CropGuard – Smart Farming")

# Sidebar Menu
menu = list(menu_items.values())
choice = st.sidebar.selectbox(translate_text("Select an option:", lang_code), menu)

# Get today's date for crop price
today_date = datetime.datetime.now().strftime('%Y-%m-%d')

if choice == menu_items["Disease Detection"]:
    st.write(translate_text("Upload plant photo to detect disease:", lang_code))
    uploaded_image = st.file_uploader("📸 Upload an image...", type=["jpg", "png", "jpeg"])
    
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # ✅ Detect disease using Gemini API
        result = detect_disease(uploaded_image)
        st.success(f"✅ {translate_text('Diagnosis:', lang_code)} {result}")

elif choice == menu_items["Weather Alerts"]:
    city = st.text_input(translate_text("Enter your city:", lang_code))
    if st.button(translate_text("Get Weather", lang_code)):
        weather_info = get_weather(city)
        st.info(weather_info)

elif choice == menu_items["Crop Prices"]:
    crop_input = st.text_input(translate_text("Enter crop name:", lang_code))

    # Map Malayalam and Hindi crop names to English
    if lang_code == "ml":
        crop = crop_name_mapping_ml.get(crop_input, crop_input)
    elif lang_code == "hi":
        crop = crop_name_mapping_hi.get(crop_input, crop_input)
    else:
        crop = crop_input

    if st.button(translate_text("Check Price", lang_code)):
        crop_price_info = get_crop_price(crop, today_date)
        translated_price_info = translate_text(crop_price_info, lang_code)
        st.info(translated_price_info)

elif choice == menu_items["Community Chatbot"]:
    user_input = st.text_input(translate_text("Ask me anything about farming:", lang_code))
    if user_input:
        response = get_chat_response(user_input, lang_code)
        translated_response = translate_text(response, lang_code)
        st.success(translated_response)

elif choice == menu_items["Resource Optimization"]:
    crop = st.text_input(translate_text("Enter crop name:", lang_code))
    if st.button(translate_text("Get Tips", lang_code)):
        optimization_tips = get_optimization_tips(crop)
        translated_tips = translate_text(optimization_tips, lang_code)
        st.info(translated_tips)
