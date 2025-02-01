import requests

AGMARKNET_API_KEY = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"

def get_crop_price(crop, date):
    """Fetch real-time crop prices from data.gov.in API"""
    url = f"https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
    
    params = {
        "api-key": AGMARKNET_API_KEY,
        "format": "json",
        "filters[commodity]": crop.upper(),
        "filters[arrival_date]": date
    }
    
    print(f"Sending request with parameters: {params}")  # Debug print
    
    response = requests.get(url, params=params)
    
    print(f"Response status code: {response.status_code}")  # Debug print
    print(f"Response content: {response.text[:500]}")  # Debug print first 500 chars
    
    if response.status_code == 200:
        data = response.json()
        if data and "records" in data and data["records"]:
            price_info = data["records"][0]
            return f"💰 {crop.capitalize()} price on {date}: ₹{price_info['modal_price']} per quintal"
        else:
            return f"⚠️ No data available for this crop/date. Total records found: {data.get('total', 0)}"
    else:
        return f"⚠️ Error fetching crop prices. Status code: {response.status_code}"

# Example usage
if __name__ == "__main__":
    crop = input("Enter crop name: ")
    date = input("Enter date (YYYY-MM-DD): ")
    print(get_crop_price(crop, date))