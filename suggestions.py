def get_optimization_tips(crop):
    tips = {
        "wheat": "🌱 Rotate crops to prevent soil depletion. Use nitrogen-rich fertilizers.",
        "rice": "💧 Optimize water usage with drip irrigation.",
        "corn": "🌞 Ensure proper sunlight exposure for maximum yield."
    }
    return tips.get(crop.lower(), "🌿 General Tip: Use organic fertilizers and monitor soil health.")
