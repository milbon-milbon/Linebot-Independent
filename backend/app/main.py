import os
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction, PostbackEvent

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

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
def handle_message(event):
    # user_idを取得する
    user_id = event.source.user_id
    # userが入力したメッセージ本体
    user_message = event.message.text

    if user_message:
        buttons_template = ButtonsTemplate(
            title="選択してください",
            text="お役に立てることはありますか",
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

#     if "医療機関を知りたい" in user_message:
#         response_message = "症状を教えてください。"
#     elif "薬について聞きたい" in user_message:
#         response_message = "薬の名前を教えてください。"
#     else:
#         response_message = "すみません、理解できませんでした。"

#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text=response_message)
#     )

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

