# import os
# import googlemaps
# from dotenv import load_dotenv
# import openai

# # Load environment variables from .env file
# load_dotenv()

# # Initialize Google Maps client
# gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))

# # Initialize OpenAI client
# openai.api_key = os.getenv("OPENAI_API_KEY")

# def find_nearby_medical_facilities(location, department, radius=1000):
#     """
#     Find nearby medical facilities based on location and department (specialty).
#     :param location: Tuple of latitude and longitude
#     :param department: Medical specialty to search for
#     :param radius: Search radius in meters
#     :return: List of places with required information
#     """
#     places = gmaps.places_nearby(location, radius=radius, keyword=department, type='hospital', language='ja')
#     results = []
    
#     for place in places.get('results', []):
#         place_id = place['place_id']
#         details = gmaps.place(place_id=place_id, language="ja")['result']
        
#         facility_info = {
#             'name': details.get('name'),
#             'address': details.get('vicinity'),
#             'phone_number': details.get('formatted_phone_number'),
#             'website': details.get('website'),
#             'opening_hours': details.get('opening_hours', {}).get('weekday_text')
#         }
#         results.append(facility_info)
    
#     return results

# def generate_response(context, user_question):
#     """
#     Generate a response from the LLM based on the context and user question.
#     :param context: Context information (e.g., list of medical facilities)
#     :param user_question: User's question
#     :return: Generated response
#     """
#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant. Provide concise and clear information based on the provided context."},
#             {"role": "user", "content": f"{context}\n\nUser question: {user_question}\n\nResponse:"}
#         ],
#         max_tokens=500,  # Increase max_tokens to handle longer responses
#         temperature=0.5,  # Lower temperature for more deterministic output
#         top_p=1
#     )
#     return response.choices[0].message['content'].strip()

# # Test the functions
# if __name__ == "__main__":
#     location = (35.6895, 139.6917)  # Example location (Tokyo)
#     department = "内科"  # Example department (Internal Medicine)
#     user_question = "近くの医療機関を教えてください。"

#     facilities = find_nearby_medical_facilities(location, department)
#     context = "\n".join([f"名前: {f['name']}, 住所: {f['address']}, 電話番号: {f['phone_number']}, ウェブサイト: {f['website']}" for f in facilities])
    
#     response = generate_response(context, user_question)
#     print(response)
import os
import googlemaps
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()

# Initialize Google Maps client
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

def find_nearby_medical_facilities(location, department, radius=1000):
    """
    Find nearby medical facilities based on location and department (specialty).
    :param location: Tuple of latitude and longitude
    :param department: Medical specialty to search for
    :param radius: Search radius in meters
    :return: List of places with required information
    """
    places = gmaps.places_nearby(location, radius=radius, keyword=department, type='hospital', language='ja')
    results = []
    
    for place in places.get('results', []):
        place_id = place['place_id']
        details = gmaps.place(place_id=place_id, language="ja")['result']
        
        facility_info = {
            'name': details.get('name'),
            'address': details.get('vicinity'),
            'phone_number': details.get('formatted_phone_number'),
            'website': details.get('website'),
            'opening_hours': details.get('opening_hours', {}).get('weekday_text')
        }
        results.append(facility_info)
    
    return results

def generate_response(context):
    """
    Generate a response from the LLM based on the context.
    :param context: Context information (e.g., list of medical facilities)
    :return: Generated response
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Provide concise and clear information based on the provided context."},
            {"role": "user", "content": f"{context}\n\nResponse:"}
        ],
        max_tokens=500,  # Increase max_tokens to handle longer responses
        temperature=0.5,  # Lower temperature for more deterministic output
        top_p=1
    )
    return response.choices[0].message['content'].strip()

# Test the functions
if __name__ == "__main__":
    location = (35.6895, 139.6917)  # Example location (Tokyo)
    department = "内科"  # Example department (Internal Medicine)

    facilities = find_nearby_medical_facilities(location, department)
    context = "\n".join([f"名前: {f['name']}, 住所: {f['address']}, 電話番号: {f['phone_number']}, ウェブサイト: {f['website']}" for f in facilities])
    
    response = generate_response(context)
    print(response)