import requests

AGMARKNET_API_KEY = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"

# Manually defined crop prices (in ₹ per quintal)
manual_prices = {
    "TOMATO": 1800,
    "MAIZE": 2200,
    "BEETROOT": 2500,
    "GINGER": 3500,
    "RICE": 3000,
    "CARROT": 2700
}

def get_crop_price(crop):
    """Fetch real-time crop prices from data.gov.in API or use manual prices."""
    url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
    date = "2025-02-02"  # Hardcoding the date as per your request
    
    params = {
        "api-key": AGMARKNET_API_KEY,
        "format": "json",
        "filters[commodity]": crop.upper(),
        "filters[arrival_date]": date
    }

    try:
        response = requests.get(url, params=params, timeout=10)  # Added timeout
        response.raise_for_status()  # Raises an error for a bad response (4xx, 5xx)

        if response.status_code == 200:
            data = response.json()
            if data and "records" in data and data["records"]:
                price_info = data["records"][0]
                return f"Price of {crop.capitalize()} on 2025-02-02: ₹{price_info['modal_price']} per quintal"
    
    except requests.exceptions.RequestException as e:
        return f"⚠️ Error fetching data: {e}"

    # Use manual price if API fails or returns no data
    if crop.upper() in manual_prices:
        return f"Price of {crop.capitalize()} on 2025-02-02: ₹{manual_prices[crop.upper()]} per quintal"
    
    return f"⚠️ No data available for {crop} on 2025-02-02."

# Example usage
if __name__ == "__main__":
    crop = input("Enter crop name: ").strip()
    print(get_crop_price(crop))
