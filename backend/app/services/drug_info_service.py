import os
import logging
from openai import OpenAI
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.models import ConversationHistory

# ロガーの設定
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# APIキーを設定
api_key = os.getenv("OPENAI_API_KEY")

# グローバル変数の定義
drug_name = "ロキソプロフェン"
info_type = "使い方"
pmda_url = "https://www.pmda.go.jp/PmdaSearch/iyakuSearch/"

# データベースセッションの取得：データベースの操作を行うためのセッション
def get_db_session() -> Session:
    return SessionLocal()

# 会話履歴を取得する関数
def get_user_conversation_history(db: Session, user_id: str):
    return db.query(ConversationHistory).filter(ConversationHistory.user_id == user_id).all()

# プロンプトを生成する関数
def generate_prompt(drug_name: str, info_type: str, pmda_url: str) -> str:
    logger.debug(f"Generating prompt for drug: {drug_name}, info type: {info_type}")
    return (f"薬剤名: {drug_name}\n"
            f"知りたい情報: {info_type}\n"
            f"以下のPMDAのURLから得られる情報を参考にして、薬についてユーザーにわかりやすい説明をしてください。\n"
            f"URL: {pmda_url}")

# 会話履歴を基にプロンプトを生成する関数
def generate_prompt_with_history(drug_name: str, info_type: str, pmda_url: str) -> str:
    conversation_history = "harukadrug"
    logger.debug(f"Generating prompt for drug: {drug_name}, info type: {info_type}, with conversation history")
    return (f"ユーザーとの過去の会話:\n{conversation_history}\n"
            f"薬剤名: {drug_name}\n"
            f"知りたい情報: {info_type}\n"
            f"以下のPMDAのURLから得られる情報を参考にして、薬についてユーザーにわかりやすい説明をしてください。\n"
            f"URL: {pmda_url}")

# 指定したプロンプトを基に、OpenAI GPTからのレスポンスを非同期に取得する関数
def generate_natural_language_response(prompt: str, model: str = "gpt-4") -> str:
    logger.info("Generating response based on the provided prompt.")
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,  # 最大500トークンまでの応答
        temperature=0.5,  # 値が0に近いほど、モデルはより決定的な応答を生成
        top_p=1  # すべてのトークンを考慮する
    )
    return response.choices[0].message.content.strip()

# check_relevance: 応答が薬品に関連しているかどうかをチェックする
def check_relevance(response: str) -> str:
    logger.debug(f"Checking relevance of response: {response}")
    if "薬" in response or "副作用" in response or "使い方" in response:
        return response
    else:
        logger.warning("Response is not relevant to the drug")
        return "薬品以外の質問には回答できません。"

# 薬剤に関する情報を取得する関数
def get_drug_info(drug_name: str, info_type: str, pmda_url: str, model: str = "gpt-4" ) -> str:
    prompt = generate_prompt_with_history(drug_name, info_type, pmda_url)
    response = generate_natural_language_response(prompt, model)
    return response

# 会話履歴を考慮して応答を生成する関数
def generate_response_with_history(user_id: str, db: Session, drug_name: str, info_type: str, pmda_url: str, model: str = "gpt-4") -> str:
    # ユーザーの会話履歴を取得
    conversation_history = get_user_conversation_history(db, user_id)
    
    # 会話履歴を整形
    formatted_history = "\n".join([f"ユーザー: {conv.user_message}\nボット: {conv.bot_response}" for conv in conversation_history])
    
    # 会話履歴を含むプロンプトを生成
    prompt = generate_prompt_with_history(drug_name, info_type, pmda_url, formatted_history)
    
    # 応答を生成
    response = generate_natural_language_response(prompt, model)
    
    return check_relevance(response)

# データベースの初期化
init_db()

# 使用例
if __name__ == "__main__":
    db_session = get_db_session()  # データベースセッションの取得
    user_id = 'example_user_id'
    response = generate_response_with_history(user_id, db_session, drug_name, info_type, pmda_url)
    print(response)
