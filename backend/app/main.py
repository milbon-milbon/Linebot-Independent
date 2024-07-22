# import os
# from fastapi import FastAPI, Request
# from dotenv import load_dotenv
# from linebot import LineBotApi, WebhookHandler
# from linebot.exceptions import InvalidSignatureError
# from linebot.models import MessageEvent, TextMessage, TextSendMessage

# # Load environment variables from .env file
# load_dotenv()

# app = FastAPI()

# line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
# handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# @app.get("/")
# async def index():
#     return "Hello, HARUKA, KU-MIN, MEME"

# @app.post("/callback")
# async def callback(request: Request):
#     signature = request.headers['X-Line-Signature']
#     body = await request.body()
#     try:
#         handler.handle(body.decode('utf-8'), signature)
#     except InvalidSignatureError:
#         return "Invalid signature. Please check your channel access token/channel secret.", 400
#     return 'OK', 200

# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     user_message = event.message.text

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
import sys
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, LocationMessage


# Load environment variables from .env file
load_dotenv()

# カレントディレクトリのパスを追加
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'services'))

from medical_facility_service import find_nearby_medical_facilities

app = FastAPI()

line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

user_data = {}

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
        raise HTTPException(status_code=400, detail="Invalid signature. Please check your channel access token/channel secret.")
    return JSONResponse(content={"message": "OK"})

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_message = event.message.text

    if "医療機関を知りたい" in user_message:
        user_data[user_id] = {'step': 'ask_specialty'}
        response_message = "診療科目を教えてください。"
    elif user_data.get(user_id, {}).get('step') == 'ask_specialty':
        user_data[user_id]['specialty'] = user_message
        user_data[user_id]['step'] = 'ask_location'
        response_message = "位置情報を送信してください。"
    else:
        response_message = "すみません、理解できませんでした。"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response_message)
    )

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    user_id = event.source.user_id
    location = (event.message.latitude, event.message.longitude)

    if user_data.get(user_id, {}).get('step') == 'ask_location':
        specialty = user_data[user_id]['specialty']
        results = find_nearby_medical_facilities(location, specialty)

        if results:
            reply_message = "近くの医療機関はこちらです：\n"
            for place in results:
                reply_message += f"名前: {place['name']}\n住所: {place['address']}\n電話番号: {place['phone_number']}\n"
                if place['website']:
                    reply_message += f"ウェブサイト: {place['website']}\n"
                if place['opening_hours']:
                    reply_message += "診療時間:\n" + "\n".join(place['opening_hours']) + "\n"
                reply_message += "\n"
        else:
            reply_message = "近くに医療機関が見つかりませんでした。"

        del user_data[user_id]
    else:
        reply_message = "すみません、理解できませんでした。"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )

# 確認用エンドポイント
@app.get("/test_location/{lat}/{lng}/{specialty}")
async def test_location(lat: float, lng: float, specialty: str):
    location = (lat, lng)
    results = find_nearby_medical_facilities(location, specialty)
    
    if results:
        reply_message = "近くの医療機関はこちらです：\n"
        for place in results:
            reply_message += f"名前: {place['name']}\n住所: {place['address']}\n電話番号: {place['phone_number']}\n"
            if place['website']:
                reply_message += f"ウェブサイト: {place['website']}\n"
            if place['opening_hours']:
                reply_message += "診療時間:\n" + "\n".join(place['opening_hours']) + "\n"
            reply_message += "\n"
    else:
        reply_message = "近くに医療機関が見つかりませんでした。"
    
    return JSONResponse(content={"message": reply_message})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)