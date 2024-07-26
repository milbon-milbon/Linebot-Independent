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
            {"role": "system", "content": 
                # くーみんさんへ: 勝手にプロンプトいじって試していました
                "あなたは、受診する医療機関に迷っている人に対して適切な提案をすることに長けた人です。今に示す提案する医療機関の候補一覧と、会話相手とのこれまでの会話履歴を参考に、今この人にもっとも適した医療機関を提案する文章を生成してください。なお、提案する文章には必ず「医療機関名」「今営業中かどうか」「電話番号」「ホームページURL（もしもURLがない場合には割愛OK）」「住所」を含めるようにしてください。それでは、よろしくお願いします。"},
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


import httpx
from fastapi import Depends, HTTPException
from .conversation_service import get_conversation_history

from app.database import SessionLocal, init_db
init_db

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_user_history(user_id: str):
    url = f"http://localhost:8000/api/conversation/{user_id}"

    async with httpx.AsyncClient() as client:
        api_response = await client.get(url)

    if api_response.status_code == 200:
        conversation_history = api_response.json
    else:
        conversation_history = None
    
    logger.debug(f"💬取得した会話履歴: {conversation_history}")
    return conversation_history

async def read_conversation(user_id: str, db: Session = Depends(get_db)):
    logger.debug(f"🚥read_conversationが呼び出されました")
    conversation = get_conversation_history(db, user_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    logger.debug("🚥正常にread_conversationの処理を終えそうです")
    return conversation


def get_nearby_hospital(location, department, user_id, db = Depends(get_db)):
    logger.debug("get_nearby hospitalが呼び出されました")
    # googlemap検索結果: 必要な引数はlocation, department
    gmap_result = find_nearby_medical_facilities(location, department)
    logger.debug("検索結果は出てきた")

    # loop = asyncio.get_event_loop()
    # conversation_history = loop.run_until_complete(read_conversation(user_id, db))
    # logger.debug(f"💬取得した会話履歴: {conversation_history}")
    conversation_history = "これまでよく通っていたのは釧路赤十字病院でした。だけど、担当の先生がいなくなてしまって他の病院を検討しています。"
    logger.debug(conversation_history)

    # LLMにpromptを投げて応答生成する: 必要な引数= context = gmap検索結果+会話履歴
    context = f"提案する医療機関の候補一覧: {gmap_result}, このユーザーとの過去の会話履歴: {conversation_history}"
    logger.debug(f"💡 LLMに渡したcontext: {context}")
    bot_response = generate_response(context)
    return bot_response
