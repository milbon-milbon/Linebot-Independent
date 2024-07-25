import os
import googlemaps
import logging
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from openai import OpenAI
from app.database import SessionLocal
from app.models import ConversationHistory

# .env ファイルから環境変数を読み込む
load_dotenv()

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# GoogleMaps初期化
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))

# OpenAI初期化
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 近くの医療施設を検索する関数定義(情報をリスト形式で返す)
def find_nearby_medical_facilities(location, department, radius=10000):
    logger.info("🌏Starting search for nearby medical facilities")
    logger.info(f"🏡Location: {location}, 🏥Department: {department}, Radius: {radius}")

    try:
        places = gmaps.places_nearby(location, radius=radius, keyword=department, type='hospital', language='ja')
        logger.info(f"🔍Found {len(places.get('results', []))} places")
    except Exception as e:
        logger.error(f"🆖An error occurred while searching for places: {e}")
        return []
    
    results = []
    
    for place in places.get('results', []):
        place_id = place['place_id']
        try:
            details = gmaps.place(place_id=place_id, language="ja")['result']
            facility_info = {
                'name': details.get('name'),
                'address': details.get('vicinity'),
                'phone_number': details.get('formatted_phone_number'),
                'website': details.get('website'),
                'opening_hours': details.get('opening_hours', {}).get('weekday_text')
            }
            results.append(facility_info)
            logger.info(f"🔍Added facility: {facility_info['name']}")
        except Exception as e:
            logger.error(f"🆖An error occurred while retrieving details for place ID {place_id}: {e}")

    logger.info(f"Returning {len(results)} results")
    return results

# OpenAIを使用して応答を生成する関数定義
def generate_response(context):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "あなたは親切なアシスタントです。指定されたエリアによって検索結果が異なる可能性があります。都市圏では半径1km、それ以外では半径10kmで検索しています。与えられたコンテキストに基づいて、簡潔で明確な情報を提供してください。"},
            {"role": "user", "content": f"{context}\n\n応答:"}
        ],
        max_tokens=500,
        temperature=0.5,
        top_p=1
    )
    return response.choices[0].message.content.strip()#client.chat.completions.create()メソッドの結果

# ユーザーの会話履歴を取得する関数定義
def get_user_conversation_history(user_id):     #REVIEW:以下変わる可能性あり
    db: Session = SessionLocal()
    history = db.query(ConversationHistory).filter(ConversationHistory.user_id == user_id).all()
    db.close()
    return history

# 会話履歴を考慮した応答生成関数定義
def generate_response_with_history(user_id, context):  #REVIEW:以下変わる可能性あり
    history = get_user_conversation_history(user_id)
    history_text = "\n".join([f"{h.timestamp}: {h.message}" for h in history])
    
    combined_context = f"過去の会話履歴:\n{history_text}\n\n現在のコンテキスト:\n{context}"
    
    return generate_response(combined_context)

# ログをテストする関数
def test_logging():
    # テスト用の位置情報と診療科目
    location = (35.6895, 139.6917)  # 東京の緯度経度
    department = "内科"
    
    # ログをキャプチャするための設定
    from io import StringIO
    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    logger.addHandler(handler)
    
    # 関数を呼び出してログを生成
    find_nearby_medical_facilities(location, department, radius=1000)
    
    # ログ出力を確認
    log_contents = log_stream.getvalue()
    print(log_contents)
    
    # ハンドラを削除
    logger.removeHandler(handler)

# テスト関数を実行
if __name__ == "__main__":
    test_logging()