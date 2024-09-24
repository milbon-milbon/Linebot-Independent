import os
import googlemaps
import logging
import httpx
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from openai import OpenAI
from fastapi import Depends, HTTPException
from app.database import SessionLocal, init_db
from app.models import ConversationHistory
from .conversation_service import get_conversation_history

# 環境変数の読み込みと初期設定
load_dotenv()

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 外部サービスのクライアント初期化
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_MAPS_API_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# データベース初期化
init_db()

def get_db():
    """データベースセッションを取得するための依存関数"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def find_nearby_medical_facilities(location, department, radius=10000):
    """
    指定された場所の近くにある医療施設を検索する

    :param location: 検索の中心となる位置（緯度、経度）
    :param department: 検索したい診療科
    :param radius: 検索半径（メートル）
    :return: 医療施設のリスト
    """
    logger.info(f"🌏 近隣の医療施設を検索: 場所 {location}, 診療科 {department}, 半径 {radius}m")

    try:
        places = gmaps.places_nearby(location, radius=radius, keyword=department, type='hospital', language='ja')
        logger.info(f"🔍 {len(places.get('results', []))}件の施設が見つかりました")
    except Exception as e:
        logger.error(f"🆖 場所の検索中にエラーが発生: {e}")
        return []
    
    results = []
    for place in places.get('results', []):
        try:
            details = gmaps.place(place_id=place['place_id'], language="ja")['result']
            facility_info = {
                'name': details.get('name'),
                'address': details.get('vicinity'),
                'phone_number': details.get('formatted_phone_number'),
                'website': details.get('website'),
                'opening_hours': details.get('opening_hours', {}).get('weekday_text')
            }
            results.append(facility_info)
            logger.info(f"🏥 施設を追加: {facility_info['name']}")
        except Exception as e:
            logger.error(f"🆖 施設詳細の取得中にエラーが発生 (ID: {place['place_id']}): {e}")

    return results

async def generate_response(context):
    """
    OpenAIを使用して応答を生成する

    :param context: 応答生成のためのコンテキスト
    :return: 生成された応答テキスト
    """
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": 
                 "あなたは、適切な医療機関を提案することに長けた専門家です。提供された医療機関の候補一覧と会話履歴を基に、最適な医療機関を提案してください。提案には必ず「医療機関名」「現在の営業状況」「電話番号」「ホームページURL（ある場合）」「住所」を含めてください。"},
                {"role": "user", "content": f"{context}\n\n応答:"}
            ],
            max_tokens=500,
            temperature=0.5,
            top_p=1
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"🆖 OpenAI APIでのレスポンス生成中にエラーが発生: {e}")
        return "申し訳ありません。レスポンスの生成中にエラーが発生しました。"

async def get_user_conversation_history(user_id: str):
    """
    ユーザーの会話履歴を取得する

    :param user_id: ユーザーID
    :return: 会話履歴
    """
    url = f"http://localhost:8000/api/conversation/{user_id}"
    try:
        async with httpx.AsyncClient() as client:
            api_response = await client.get(url)
        if api_response.status_code == 200:
            return api_response.json()
        else:
            logger.warning(f"💬 会話履歴の取得に失敗: ステータスコード {api_response.status_code}")
            return None
    except Exception as e:
        logger.error(f"🆖 会話履歴の取得中にエラーが発生: {e}")
        return None

async def read_conversation(user_id: str, db: Session = Depends(get_db)):
    """
    ユーザーの会話履歴を読み取る

    :param user_id: ユーザーID
    :param db: データベースセッション
    :return: 会話履歴
    """
    logger.debug(f"🚥 read_conversationが呼び出されました: ユーザーID {user_id}")
    conversation = get_conversation_history(db, user_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="会話履歴が見つかりません")
    logger.debug("🚥 正常にread_conversationの処理を完了しました")
    return conversation

async def get_nearby_hospital(location, department, user_id, db = Depends(get_db)):
    """
    近くの病院を検索し、ユーザーに最適な医療機関を提案する

    :param location: 検索の中心となる位置
    :param department: 検索したい診療科
    :param user_id: ユーザーID
    :param db: データベースセッション
    :return: 生成された提案レスポンス
    """
    logger.debug("🏥 get_nearby_hospitalが呼び出されました")

    # Google Maps APIを使用して近隣の医療施設を検索
    gmap_result = await find_nearby_medical_facilities(location, department)
    logger.debug(f"🔍 {len(gmap_result)}件の医療施設が見つかりました")

    # ユーザーの会話履歴を取得
    # 注意: 以下はテスト用のダミーデータです。実際の実装では、この部分を適切に置き換えてください。
    conversation_history = "これまでよく通っていたのは釧路赤十字病院でした。だけど、担当の先生がいなくなてしまって他の病院を検討しています。"
    logger.debug(f"💬 ユーザーの会話履歴: {conversation_history}")

    # OpenAI APIを使用して最適な医療機関を提案
    context = f"提案する医療機関の候補一覧: {gmap_result}, このユーザーとの過去の会話履歴: {conversation_history}"
    logger.debug(f"💡 OpenAI APIに送信するコンテキスト: {context}")
    bot_response = await generate_response(context)

    return bot_response

# ログのテスト関数（開発時のみ使用）
def test_logging():
    """ロギング機能をテストする関数"""
    location = (35.6895, 139.6917)  # 東京の緯度経度
    department = "内科"
    
    from io import StringIO
    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    logger.addHandler(handler)
    
    find_nearby_medical_facilities(location, department, radius=1000)
    
    log_contents = log_stream.getvalue()
    print(log_contents)
    
    logger.removeHandler(handler)

if __name__ == "__main__":
    test_logging()