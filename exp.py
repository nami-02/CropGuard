import streamlit as st
from langdetect import detect
from googletrans import Translator
import datetime
from PIL import Image

# Set page config
st.set_page_config(
    page_title="CropGuard",
    page_icon="🌾",
    layout="wide"
)

# Import necessary modules
from weather_api import get_weather
from price_api import get_crop_price
from chatbot import get_chat_response
from disease_model import detect_disease
#from pest import analyze_soil  # New module for soil report processing
from soilrep import analyze_soil


# Custom CSS for styling
st.markdown("""
    <style>
    /* Main container */
    .main {
        padding: 0 !important;
    }
    
    /* Hero section */
    .hero-section {
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1523348837708-15d4a09cfac2');
        background-size: cover;
        background-position: center;
        padding: 6rem;
        color: white;
        text-align: center;
        margin: -4rem -4rem 1rem -4rem;
    }
    
    /* Buttons */
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 4px;
        cursor: pointer;
    }
    
    .stButton button:hover {
        background-color: #45a049;
    }
    
    /* Content section */
    .content-section {
        padding: 1rem;
        margin-top: 0.5rem;
    }

    /* Adjust heading spacing */
    .stHeadingContainer {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Hero section with background image
st.markdown("""
    <div class="hero-section">
        <h1>🌾 CropGuard - Your Farming Assistant</h1>
        <p>Empowering farmers with the best tools for disease detection, crop prices, weather alerts, and soil analysis.</p>
    </div>
""", unsafe_allow_html=True)


# Initialize Translator
translator = Translator()

# Language Selection
language_options = {"English": "en", "Hindi": "hi", "Malayalam": "ml"}
selected_lang = st.sidebar.radio("Choose Language:", list(language_options.keys()))
lang_code = language_options[selected_lang]

# Translation Helper
def translate_text(text, target_lang):
    if target_lang == "en":
        return text
    translation = translator.translate(text, dest=target_lang)
    return translation.text

# Menu items with language support
menu_items = {
    "Disease Detection": translate_text("Disease Detection", lang_code),
    "Weather Alerts": translate_text("Weather Alerts", lang_code),
    "Crop Prices": translate_text("Crop Prices", lang_code),
    "Community Chatbot": translate_text("Community Chatbot", lang_code),
    "Soil Report": translate_text("Soil Report", lang_code)  # New option added
}

# Sidebar Menu
menu = list(menu_items.values())
choice = st.sidebar.selectbox(translate_text("Select an option:", lang_code), menu)

# Main content section
st.markdown('<div class="content-section">', unsafe_allow_html=True)

if choice == menu_items["Disease Detection"]:
    st.subheader("🌾 " + translate_text("Disease Detection", lang_code))
    uploaded_image = st.file_uploader(translate_text("Upload Image of Crop:", lang_code), type=["jpg", "jpeg", "png"])
    
    if uploaded_image:
        img = Image.open(uploaded_image)
        
        # Display the image using Streamlit
        st.image(img, caption=translate_text("Uploaded Image", lang_code), use_column_width=True) 
                
        result = detect_disease(uploaded_image)
        translated_result = translate_text(result, lang_code)
        st.success(f"✅ {translate_text('Disease Detected:', lang_code)} {translated_result}")

elif choice == menu_items["Weather Alerts"]:
    st.subheader("🌦 " + translate_text("Weather Alerts", lang_code))
    location = st.text_input(translate_text("Enter your Location:", lang_code))
    
    if location:
        weather_data = get_weather(location)
        st.write(weather_data)

elif choice == menu_items["Crop Prices"]:
    st.subheader("💰 " + translate_text("Crop Prices", lang_code))
    
    # Input field for crop name instead of a selectbox
    crop_type = st.text_input(translate_text("Enter Crop Name:", lang_code))
    
    # Input field for date
    #date = st.text_input(translate_text("Enter Date (YYYY-MM-DD):", lang_code))
    
    if crop_type:
        crop_price = get_crop_price(crop_type)
        st.write(crop_price)

elif choice == menu_items["Community Chatbot"]:
    st.subheader("💬 " + translate_text("Community Chatbot", lang_code))
    user_query = st.text_input(translate_text("Ask me anything about crops or farming!", lang_code))
    
    if user_query:
        response = get_chat_response(user_query)
        translated_response = translate_text(response, lang_code)
        st.write(translated_response)

elif choice == menu_items["Soil Report"]:
    st.subheader("🌱 " + translate_text("Soil Report", lang_code))
    
    # Soil Parameter Inputs
    nitrogen = st.number_input(translate_text("Enter Nitrogen (N) level in ppm:", lang_code), min_value=0.0)
    phosphorus = st.number_input(translate_text("Enter Phosphorus (P) level in ppm:", lang_code), min_value=0.0)
    potassium = st.number_input(translate_text("Enter Potassium (K) level in ppm:", lang_code), min_value=0.0)
    ph_level = st.number_input(translate_text("Enter pH level of the soil:", lang_code), min_value=0.0, max_value=14.0)
    
    # Crop type selection for soil analysis
    crop_type = st.selectbox(translate_text("Select Crop Type:", lang_code), ["Rice", "Wheat", "Maize"])
    
    if st.button(translate_text("Get Recommendations", lang_code)):
        if nitrogen and phosphorus and potassium and ph_level and crop_type:
            recommendations = analyze_soil(nitrogen, phosphorus, potassium, ph_level, crop_type)
            st.success(f"✅ {translate_text('Recommendations:', lang_code)} {recommendations}")
        else:
            st.error(translate_text("Please fill in all the fields.", lang_code))

st.markdown('</div>', unsafe_allow_html=True)

# Implementing helper functions for each feature
def get_weather(location):
    # Placeholder function for weather API
    return f"Weather data for {location} coming soon!"

def get_crop_price(crop_type):
    # Placeholder function for crop price API
    return f"Price data for {crop_type} coming soon!"

def get_chat_response(query):
    # Placeholder function for chatbot
    return f"Response to your query: {query}"

def detect_disease(image):
    # Placeholder function for disease detection
    return f"Disease detected in the crop image."

# New analyze_soil function
def analyze_soil(nitrogen, phosphorus, potassium, ph_level, crop_type):
    """
    Placeholder function for analyzing soil.
    This is where the actual soil report analysis logic would go.
    """
    # Simulate a recommendation based on soil parameters
    recommendation = f"Based on the soil parameters, for crop {crop_type}, we recommend adjusting fertilizer levels."
    if nitrogen < 20:
        recommendation += " Increase Nitrogen fertilizer."
    if phosphorus < 15:
        recommendation += " Increase Phosphorus fertilizer."
    if potassium < 30:
        recommendation += " Increase Potassium fertilizer."
    if ph_level < 6:
        recommendation += " Consider adding lime to raise pH."
    
    return recommendation
