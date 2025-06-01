from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os
from geopy.geocoders import Nominatim
import json
from huggingface_hub import InferenceClient
api_key = os.getenv("HUGGINGFACE_API_KEY")

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure OpenAI with new client

client = InferenceClient(
    provider="fireworks-ai",
    #api_key=api_key,
    api_key=api_key,
)

def get_coordinates(place_name):
    try:
        geolocator = Nominatim(user_agent="trip_planner")
        location = geolocator.geocode(place_name)
        if location:
            return {"lat": location.latitude, "lng": location.longitude}
        return None
    except Exception as e:
        print(f"Error getting coordinates for {place_name}: {str(e)}")
        return None

def parse_itinerary(itinerary_text):
    """Parse the itinerary text and extract places."""
    places = []
    lines = itinerary_text.strip().split('\n')
    current_day = None
    
    for line in lines:
        if line.startswith('Day'):
            current_day = line.strip(':')
        elif ':' in line and current_day:
            try:
                time_part, details = line.split(':', 1)
                place_parts = details.split('-')
                if len(place_parts) >= 1:
                    place_name = place_parts[0].strip()
                    cost = place_parts[1].strip() if len(place_parts) > 1 else "N/A"
                    transport = place_parts[2].strip() if len(place_parts) > 2 else "N/A"
                    
                    coordinates = get_coordinates(place_name)
                    if coordinates:
                        places.append({
                            "day": current_day,
                            "time": time_part.strip(),
                            "place": place_name,
                            "cost": cost,
                            "transport": transport,
                            "coordinates": coordinates
                        })
            except Exception as e:
                print(f"Error parsing line: {line}, Error: {str(e)}")
                continue
    
    return places

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    destination = data.get('destination')
    duration = data.get('duration')
    budget = data.get('budget')

    # Create the prompt for OpenAI
    prompt = f"""Create a detailed day-by-day itinerary for a {duration} trip to {destination} with a budget of Rs. {budget}.
    Format the response exactly as follows for each day:
    Day X:
    HH:MM: Place - Cost in Rs. - Mode of Transport
    
    Include popular tourist attractions, local experiences, and meals. Ensure all costs add up to within the budget.
    Make times realistic and include travel times between locations."""

    try:
        # Using the new OpenAI client formatsdsd
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-R1-0528",
            messages=[
                {"role": "system", "content": "You are a travel planning expert who creates detailed itineraries."},
                {"role": "user", "content": prompt}
            ],
        )
        
        itinerary_text = response.choices[0].message.content
        places_with_coordinates = parse_itinerary(itinerary_text)
        
        # Get coordinates for the main destination for initial map view
        main_coordinates = get_coordinates(destination)
        
        return jsonify({
            "itinerary": itinerary_text,
            "places": places_with_coordinates,
            "main_coordinates": main_coordinates
        })

    except Exception as e:
        print(f"OpenAI API Error: {str(e)}")  # Add detailed error logging
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 