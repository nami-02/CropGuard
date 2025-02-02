import requests
from googletrans import Translator  # To handle translation

# Your API key directly in the code
GROQ_API_KEY = "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"  # Replace with your actual API key

# Initialize the Translator for Google Translate API
translator = Translator()

def translate_text(text, target_lang="en"):
    """Translate text to the target language."""
    if target_lang == "en":
        return text  # No need to translate if it's already in English
    translation = translator.translate(text, dest=target_lang)
    return translation.text  # Accessing the 'text' attribute of the translation result

def improve_response_clarity(response):
    """Enhance the response to make it clearer and more structured."""
    # You can define specific improvements here. For example, structured formatting:
    if "watering" in response.lower():
        response = "Here’s how to water your plants properly:\n" + response
    return response

def get_chat_response(user_input, lang_code="en"):
    """
    Get a response from Groq API, while handling different languages.
    Args:
        user_input (str): The input prompt from the user.
        lang_code (str): Language code (default is "en" for English).
    Returns:
        str: The model's response or error message.
    """
    
    # Translate the input if it's not in English
    if lang_code != "en":
        user_input = translate_text(user_input, "en")  # Translate to English before passing

    # Send the request to the Groq API
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {
                "role": "user",
                "content": user_input
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1024,
        "top_p": 1,
        "stream": False
    }
    
    try:
        # Make the POST request to the Groq API
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        # Get the response from the API
        result = response.json()
        response_content = result["choices"][0]["message"]["content"]
        
        # Improve the clarity of the response
        response_content = improve_response_clarity(response_content)
        
        # Translate the response if needed (back to the original language)
        if lang_code != "en":
            response_content = translate_text(response_content, lang_code)
        
        return response_content
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Error making request: {str(e)}"
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_details = e.response.json()
                error_msg += f"\nAPI Error: {error_details}"
            except ValueError:
                error_msg += f"\nAPI Response: {e.response.text}"
        return error_msg

# Example usage
if __name__ == "__main__":
    user_input = "What is the capital of France?"
    response = get_chat_response(user_input, "hi")  # Example with Hindi language
    print("Response:", response)
