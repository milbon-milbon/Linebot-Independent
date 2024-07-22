import os
import googlemaps
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Google Maps client
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))

def find_nearby_medical_facilities(location, keyword, radius=1000):#(location, department)
    """
    Find nearby medical facilities based on location and keyword (specialty).
    :param location: Tuple of latitude and longitude
    :param keyword: Medical specialty to search for
    :param radius: Search radius in meters
    :return: List of places with required information
    """
    places = gmaps.places_nearby(location, radius=radius, keyword=keyword, type='hospital')
    results = []
    
    for place in places.get('results', []):
        place_id = place['place_id']
        details = gmaps.place(place_id=place_id)['result']
        
        facility_info = {
            'name': details.get('name'),
            'address': details.get('vicinity'),
            'phone_number': details.get('formatted_phone_number'),
            'website': details.get('website'),
            'opening_hours': details.get('opening_hours', {}).get('weekday_text')
        }
        results.append(facility_info)
    
    return results

# テストやデバッグのためのモジュールのため、一旦コメントアウト
# Example usage
# if __name__ == "__main__":
#     location = (35.6895, 139.6917)  # Tokyo's latitude and longitude
#     results = find_nearby_medical_facilities(location)
#     for place in results:
#         print(place['name'], place['vicinity'])

