import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
import requests
import json
import asyncio
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, LocationMessage,
    QuickReply, QuickReplyButton, MessageAction, LocationAction
)
from .services.medical_facility_service import find_nearby_medical_facilities
from .services.drug_info_service import get_drug_info
from app.views import router as conversation_router
from app.logging_config import logger
from .post_conversation import save_conversation_history

load_dotenv()
app = FastAPI()


# 例外処理の追加
line_bot_api = None
handler = None

try:
    line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
    handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
    logger.debug(f"📍line_bot_api: {line_bot_api}")
    logger.debug(f"📍handler: {handler}")
except Exception:
    logger.error(f"環境変数の読み込みに失敗しました: {Exception}")

user_context = {}

# サーバー起動確認用のコード
@app.get("/")
async def index():
    return "Hello, HARUKA, KU-MIN, MEME"

@app.post("/callback/")
async def callback(request: Request):
    signature = request.headers['X-Line-Signature']
    body = await request.body()
    try:
        logger.debug("📩メッセージを受信しました。")
        logger.debug(f"📝 メッセージ内容: {body.decode('utf-8')}")
        handler.handle(body.decode('utf-8'), signature)
    except InvalidSignatureError:
        return PlainTextResponse("Invalid signature. Please check your channel access token/channel secret.", status_code=400)
    return PlainTextResponse('OK', status_code=200)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    logger.debug("📣handle_messageが呼び出されました。") 
    logger.debug(f"✅event: {event}")
    try:
        user_id = event.source.user_id
        user_message = event.message.text

        logger.debug(f"ℹ️ user_id: {user_id}")
        logger.debug(f"💬 メッセージ: {user_message}")

        quick_reply_buttons = [
            QuickReplyButton(action=MessageAction(label="医療機関を知りたい", text="医療機関を知りたい")),
            QuickReplyButton(action=MessageAction(label="薬について聞きたい", text="薬について聞きたい"))
        ]

        quick_reply = QuickReply(items=quick_reply_buttons)

        departments = ["内科", "整形外科", "耳鼻科", "眼科", "皮膚科", "泌尿器科", "婦人科", "精神科"]

        if user_message == "医療機関を知りたい":
            bot_response = "承知しました。何科を受診したいですか？"

            quick_reply_department = [
                QuickReplyButton(action=MessageAction(label="内科", text="内科")),
                QuickReplyButton(action=MessageAction(label="整形外科", text="整形外科")),
                QuickReplyButton(action=MessageAction(label="耳鼻科", text="耳鼻科")),
                QuickReplyButton(action=MessageAction(label="眼科", text="眼科")),
                QuickReplyButton(action=MessageAction(label="皮膚科", text="皮膚科")),
                QuickReplyButton(action=MessageAction(label="婦人科", text="婦人科")),
                QuickReplyButton(action=MessageAction(label="泌尿器科", text="泌尿器科")),
                QuickReplyButton(action=MessageAction(label="精神科", text="精神科")),
            ]

            quick_reply = QuickReply(items=quick_reply_department)

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=bot_response, quick_reply=quick_reply)
            )

        elif user_message in departments:
            logger.debug("🗺️ 位置情報送信依頼をします")
            user_context[user_id] = {'selected_department': user_message}
            bot_response = f"{user_message}ですね。それではお近くの医療機関を検索しますので、位置情報を送信してください。"
            # 位置情報の送信を促す
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(
                    text=bot_response,
                    quick_reply=QuickReply(
                        items=[
                            QuickReplyButton(action=LocationAction(label="位置情報を送信", text="位置情報を送信"))
                        ]
                    )
                )
            )

        elif user_message == "薬について聞きたい":
            bot_response = "私が提供できるのはお薬の副作用または使い方についてです。調べたいお薬の名前をできるだけ正確に教えてください。"
            user_context[user_id] = {'awaiting_drug_name': True}
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=bot_response)
            )

        elif user_context.get(user_id, {}).get('awaiting_drug_name'):
            drug_name = user_message
            user_context[user_id] = {'drug_name': drug_name, 'awaiting_info_type': True}
            bot_response = "そのお薬について、副作用、使い方のどちらを調べますか？"
            quick_reply_info_type = QuickReply(items=[
                QuickReplyButton(action=MessageAction(label="副作用", text="副作用")),
                QuickReplyButton(action=MessageAction(label="使い方", text="使い方"))
            ])
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=bot_response, quick_reply=quick_reply_info_type)
            )

        elif user_context.get(user_id, {}).get('awaiting_info_type'):
            info_type = user_message
            drug_name = user_context[user_id].get('drug_name')
            user_context[user_id] = {}
            if info_type in ["副作用", "使い方"]:
                logger.debug(f"💊薬剤名: {drug_name}")
                logger.debug(f"💊知りたいこと: {info_type}")
                bot_response = get_drug_info(drug_name, info_type, "https://www.pmda.go.jp/PmdaSearch/iyakuSearch/GeneralList?keyword=" + drug_name)
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=bot_response)
                )
            else:
                bot_response = "無効な選択です。もう一度お試しください。"
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=bot_response)
                )

        else:
            bot_response = "お役に立てることはありますか？"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=bot_response, quick_reply=quick_reply)
            )

        # 会話履歴を保存するリクエストを /conversation に送信する
        conversation_data = {
            "user_id": user_id,
            "user_message": user_message,
            "bot_response": bot_response
        }

        logger.debug(f"💬会話履歴: {conversation_data}")

        # 非同期関数を同期関数の中で呼び出す
        asyncio.run(save_conversation_history(conversation_data))
        
    except Exception as e:
        logger.error(f"❌ エラー発生: {e}")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="申し訳ありませんが、処理中にエラーが発生しました。")
        )

@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    user_id = event.source.user_id
    if isinstance(event.message, LocationMessage):
            logger.info("📍位置情報を受信しました。")
            logger.debug(f"位置情報メッセージの内容: {event.message}")
            latitude = event.message.latitude
            longitude = event.message.longitude
            user_department = user_context.get(user_id, {}).get('selected_department')

            if user_department:
                location = (latitude, longitude)
                logger.debug(f"🏥 診療科(department): {user_department}")
                logger.debug(f"📍 位置情報: {location}")
                try:
                    results = find_nearby_medical_facilities(location, user_department)
                    if results:
                        response = "お近くの医療機関はこちらです：\n\n" + "\n\n".join(
                            [f"{facility['name']}\n住所: {facility['address']}\n電話番号: {facility.get('phone_number', 'N/A')}\nウェブサイト: {facility.get('website', 'N/A')}" for facility in results]
                        )
                    else:
                        response = "お近くに該当する医療機関が見つかりませんでした。"
                except Exception as e:
                    logger.error(f"❌医療機関検索中のエラー発生: {e}")
                    response = "医療機関の検索中にエラーが発生しました。"

            else:
                response = "診療科目が選択されていません。もう一度お試しください。"

            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=response)
            )
            
            # # ここでも、会話履歴を保存するリクエストを/conversation..に送信する

    

# 会話履歴を保存するエンドポイント処理
app.include_router(conversation_router, prefix="/api")

