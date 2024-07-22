import os
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction, PostbackEvent
from app.services.medical_facility_service import find_medical_facilities
from app.services.drug_info_service import get_drug_info

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

user_context = {}

# サーバー起動確認用のコード
@app.get("/")
async def index():
    return "Hello, HARUKA, KU-MIN, MEME"

@app.post("/callback")
async def callback(request: Request):
    signature = request.headers['X-Line-Signature']
    body = await request.body()
    try:
        handler.handle(body.decode('utf-8'), signature)
    except InvalidSignatureError:
        return "Invalid signature. Please check your channel access token/channel secret.", 400
    return 'OK', 200

@handler.add(MessageEvent, message=TextMessage)
async def handle_message(event):
    # user_idを取得する
    user_id = event.source.user_id
    # userが入力したメッセージ本体
    user_message = event.message.text

    if user_id in user_context:
        # user_context = {}
        context = user_context[user_id]

        if context == "medical":
            response = await find_medical_facilities(user_message)
        elif context == "drug_info":
            response = await get_drug_info(user_message)
        else:
            response = "すみません、理解できませんでした"

        # line_botのリプ
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response)
        )

        del user_context[user_id]
    
    else:
        buttons_template = ButtonsTemplate(
            title="選択してください",
            text="お役に立てることはありますか？",
            actions=[
                PostbackAction(label="医療機関を知りたい", data="medical"),
                PostbackAction(label="薬について聞きたい", data="drug_info")
            ]
        )

        template_message = TemplateSendMessage(
            alt_text="選択してください",
            template=buttons_template
        )

        line_bot_api.reply_message(
            event.reply_token,
            template_message
        )

    print(f"user_id: {user_id}")
    print(f"メッセージ: {user_message}")

@handler.add(PostbackEvent)
async def handle_postback(event):
    postback_data = event.postback.data
    user_id = event.source.user_id

    if postback_data == "medical":
        reply_message = "何科の受診をご希望ですか？"
        user_context[user_id] = "medical"
    elif postback_data == "drug_info":
        reply_message = "何というお薬の、どのようなことについてお調べしますか？"
        user_context[user_id] = "drug_info"
    else:
        reply_message = "すみません、理解できませんでした。"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )

    print(f"postback_data: {postback_data}")