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

# # 近隣の医療機関を検索する関数
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
# #LLMを使用して自然言語で応答を生成する関数
# def generate_response(context):
#     """
#     Generate a response from the LLM based on the context.
#     :param context: Context information (e.g., list of medical facilities)
#     :return: Generated response
#     """
#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         messages=[
#             {"role": "system", "content": "あなたは親切なアシスタントです。与えられたコンテキストに基づいて、簡潔で明確な情報を提供してください。"},
#             {"role": "user", "content": f"{context}\n\n応答:"}
#         ],
#         max_tokens=500,  # 最大500トークンまでの応答
#         temperature=0.5,  # 値が0に近いほど、モデルはより決定的な（同じプロンプトに対して同じ応答を生成する）応答を生成
#         top_p=1 #すべてのトークンを考慮する（フィルタリングしない）
#     )
#     return response.choices[0].message['content'].strip()

# # Test the functions
# if __name__ == "__main__":
#     location = (35.6895, 139.6917)  # Example location (Tokyo)
#     department = "内科"  # Example department (Internal Medicine)

#     facilities = find_nearby_medical_facilities(location, department)
#     context = "\n".join([f"名前: {f['name']}, 住所: {f['address']}, 電話番号: {f['phone_number']}, ウェブサイト: {f['website']},営業時間: {f['opening_hours']}," for f in facilities])
    
#     response = generate_response(context)
#     print(response)


import os
import googlemaps
from dotenv import load_dotenv
from openai import OpenAI, AsyncOpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize Google Maps client
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

async def generate_response(context):
    """
    Generate a response from the LLM based on the context.
    :param context: Context information (e.g., list of medical facilities)
    :return: Generated response
    """
    async_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = await async_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "あなたは親切なアシスタントです。与えられたコンテキストに基づいて、簡潔で明確な情報を提供してください。"},
            {"role": "user", "content": f"{context}\n\n応答:"}
        ],
        max_tokens=500,
        temperature=0.5,
        top_p=1
    )
    return response.choices[0].message.content.strip()

# Test the functions
if __name__ == "__main__":
    import asyncio
    location = (35.6895, 139.6917)  # Example location (Tokyo)
    department = "外科"  # Example department (Internal Medicine)

    facilities = find_nearby_medical_facilities(location, department)
    context = "\n".join([f"名前: {f['name']}, 住所: {f['address']}, 電話番号: {f['phone_number']}, ウェブサイト: {f['website']}, 営業時間: {f['opening_hours']}" for f in facilities])
    
    response = asyncio.run(generate_response(context))
    print(response)
