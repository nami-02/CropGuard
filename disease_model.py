import mimetypes
from PIL import Image
from io import BytesIO
import google.generativeai as genai

# ✅ Replace with your actual API key
GEMINI_API_KEY = "AIzaSyCSrd3og7if7Ui7aAoonPLxy6JEli3uZvg"

genai.configure(api_key=GEMINI_API_KEY)

# ✅ Use a valid Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")  # You can also try "gemini-1.5-pro"

# Function to get disease diagnosis from image
def detect_disease(uploaded_image):
    if uploaded_image is None:
        return "❌ No file uploaded."

    # Check the size of the uploaded file
    uploaded_image.seek(0)  # Move to the start of the file
    image_data = uploaded_image.read()

    # Check if image data is empty
    if len(image_data) == 0:
        return "❌ The uploaded image is empty or corrupt."

    # Debug: Print size of the uploaded image
    print(f"Image uploaded. Size: {len(image_data)} bytes")

    try:
        # Try to open the image
        image = Image.open(BytesIO(image_data))  # Convert bytes to an image object
        image.show()  # This will show the image if it is successfully loaded
    except Exception as e:
        return f"❌ Error opening image: {e}"

    # If the image opened successfully, proceed
    prompt = "Identify the plant disease and suggest an organic treatment."
    response = model.generate_content([prompt, image])
    return response.text

# Example usage in your script (replace `uploaded_image` with actual file):
# uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
# if uploaded_image is not None:
#     result = diagnose_disease(uploaded_image)
#     st.write(result)
