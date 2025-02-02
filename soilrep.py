import google.generativeai as genai

# Configure the Gemini API key
genai.configure(api_key="AIzaSyCechdSJRU97rM554e9nxGpukKDWehxwTE")  # Replace with your actual API key

def get_soil_analysis(nitrogen, phosphorus, potassium, ph_level, crop_type):
    # Generate prompt for the Gemini API using the soil data and crop type
    prompt = f"""Give fertilizer and pesticide recommendations for a crop with Nitrogen: {nitrogen}, Phosphorus: {phosphorus}, Potassium: {potassium}, pH: {ph_level}, and crop type: {crop_type}."""
    
    try:
        # Call Gemini API to generate the response
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

        # Log the full response for inspection
        print("Full API Response:", response)

        # Check if the response contains candidates
        if hasattr(response, 'candidates') and len(response.candidates) > 0:
            candidate = response.candidates[0]
            if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts') and len(candidate.content.parts) > 0:
                # Access the first part of the content
                content = candidate.content.parts[0].text if hasattr(candidate.content.parts[0], 'text') else ""
                if content:
                    return content
                else:
                    return "Error: No meaningful content found in the response."
            else:
                return "Error: No content parts found in the response."
        else:
            return "Error: No candidates found in the response."
    
    except Exception as e:
        return f"Error occurred while generating the soil analysis: {str(e)}"

# Function to process soil data and generate recommendations
def analyze_soil(nitrogen, phosphorus, potassium, ph_level, crop_type):
    # Get soil analysis from Gemini API
    recommendations = get_soil_analysis(nitrogen, phosphorus, potassium, ph_level, crop_type)
    
    return recommendations

# Example usage with sample data
response = analyze_soil(100, 50, 30, 6.5, "Rice")
print(response)
