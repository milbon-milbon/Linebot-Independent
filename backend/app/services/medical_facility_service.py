import os
import googlemaps
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Google Maps client
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))

def find_nearby_medical_facilities(location, radius=1000):
    """
    Find nearby medical facilities based on location.
    :param location: Tuple of latitude and longitude
    :param radius: Search radius in meters
    :return: List of places
    """
    places = gmaps.places_nearby(location, radius=radius, type='hospital')
    return places.get('results', [])

# Example usage
if __name__ == "__main__":
    location = (35.6895, 139.6917)  # Tokyo's latitude and longitude
    results = find_nearby_medical_facilities(location)
    for place in results:
        print(place['name'], place['vicinity'])

