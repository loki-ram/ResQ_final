from flask import Flask, jsonify, request
import requests

vol = Flask(__name__)

# Secure your API keys (use environment variables in production)
OPENWEATHER_API_KEY = "f45747782f9dbb145b7e866c825ebf5b"
FEMA_ENDPOINT = "https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries"

@vol.route('/disaster-alerts', methods=['GET'])
def disaster_alerts():
    location = request.args.get('location', 'New York')  # Default location

    # Fetch data from OpenWeather API
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&volid={OPENWEATHER_API_KEY}"
    try:
        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()  # Raise exception for HTTP errors
        weather_data = weather_response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching weather data: {str(e)}"}), 500

    # Fetch data from FEMA API
    try:
        fema_response = requests.get(FEMA_ENDPOINT)
        fema_response.raise_for_status()
        fema_data = fema_response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching FEMA data: {str(e)}"}), 500

    # Combine results
    result = {
        "weather": weather_data.get('weather', []),
        "fema_disasters": fema_data.get('DisasterDeclarationsSummaries', [])
    }

    return jsonify(result)

if __name__ == '__main__':
    vol.run(debug=True)
