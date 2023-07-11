# Dependencies
import requests
import json
import time

# Import the API key
from config import geoapify_key

def single_geocode(target):
    # Target location
    target_city = target

    # Build the endpoint URL
    target_url = f"https://api.geoapify.com/v1/geocode/search?text={target_city}&format=json&apiKey={geoapify_key}"

    # Run a request to endpoint and convert result to json
    geo_data = requests.get(target_url).json()

    # Extract latitude and longitude
    lat = geo_data["results"][0]["lat"]
    lon = geo_data["results"][0]["lon"]

    # Adds a time buffer to slow down API requests when using this in a for loop
    time.sleep(1)

    # Return the results
    return lat, lon