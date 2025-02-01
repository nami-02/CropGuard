import streamlit as st
import datetime
from langdetect import detect
from googletrans import Translator

# Set page config at the very beginning
st.set_page_config(page_title="CropGuard", page_icon="🌾")

# Import custom modules (you need to implement these)
from weather_api import get_weather
from price_api import get_crop_price
from chatbot import get_chat_response
from suggestions import get_optimization_tips

# Initialize Translator
translator = Translator()

# 🌍 Language Selection
language_options = {"English": "en", "Hindi": "hi", "Malayalam": "ml"}
selected_lang = st.sidebar.radio("🌐 Choose Language:", list(language_options.keys()))
lang_code = language_options[selected_lang]  # Now lang_code is assigned here

# 🔤 Translation Helper
def translate_text(text, target_lang):
    if target_lang == "en":
        return text  # No need to translate if it's already English
    translation = translator.translate(text, dest=target_lang)
    return translation.text  # Accessing the 'text' attribute of the translation result

# UI Elements with Language Support
menu_items = {
    "Disease Detection": translate_text("Disease Detection", lang_code),
    "Weather Alerts": translate_text("Weather Alerts", lang_code),
    "Crop Prices": translate_text("Crop Prices", lang_code),
    "Community Chatbot": translate_text("Community Chatbot", lang_code),
    "Resource Optimization": translate_text("Resource Optimization", lang_code)
}

st.title("🌾 CropGuard – AI-Powered Smart Farming")

# Sidebar Menu
menu = list(menu_items.values())
choice = st.sidebar.selectbox(translate_text("Select an option:", lang_code), menu)

# Get today's date (or any specific date you want for crop price)
today_date = datetime.datetime.now().strftime('%Y-%m-%d')

if choice == menu_items["Disease Detection"]:
    # You would use your own disease detection code here
    st.write(translate_text("Upload plant photo to detect disease:", lang_code))
    # uploaded_image = st.file_uploader("Upload an image...", type=["jpg", "png", "jpeg"])
    # if uploaded_image:
    #     image = Image.open(uploaded_image)
    #     st.image(image, caption="Uploaded Image", use_column_width=True)
    #     result = predict_disease(image)
    st.success(f"✅ {translate_text('Diagnosis:', lang_code)} {'Plant disease name'}")

elif choice == menu_items["Weather Alerts"]:
    city = st.text_input(translate_text("Enter your city:", lang_code))
    if st.button(translate_text("Get Weather", lang_code)):
        weather_info = get_weather(city)
        st.info(weather_info)

elif choice == menu_items["Crop Prices"]:
    crop = st.text_input(translate_text("Enter crop name (e.g., wheat, rice, corn):", lang_code))
    if st.button(translate_text("Check Price", lang_code)):
        # Pass both crop name and today's date to get_crop_price function
        crop_price_info = get_crop_price(crop, today_date)
        st.info(crop_price_info)

elif choice == menu_items["Community Chatbot"]:
    user_input = st.text_input(translate_text("Ask me anything about farming:", lang_code))
    if user_input:
        response = get_chat_response(user_input, lang_code)  # Pass selected language code to chatbot
        st.success(response)

elif choice == menu_items["Resource Optimization"]:
    crop = st.text_input(translate_text("Enter crop name:", lang_code))
    if st.button(translate_text("Get Tips", lang_code)):
        optimization_tips = get_optimization_tips(crop)
        st.info(optimization_tips)
