import os
from fastapi import FastAPI, Request
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction, PostbackEvent, LocationSendMessage
from .services.medical_facility_service import find_nearby_medical_facilities
from .services.drug_info_service import get_drug_info

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

# 実際の検索ロジックを含む関数を飛び出す処理: contextが揃っている場合
@handler.add(MessageEvent, message=TextMessage)
async def handle_message(event):
    # user_idを取得する
    user_id = event.source.user_id
    # userが入力したメッセージ本体
    user_message = event.message.text

    # contextにuser_idが含まれている場合
    if user_id in user_context:
        # user_context[user_id] = user_idごとのcontextを保持し、userのstateをtracking
        context = user_context[user_id]

        # 医療機関情報の検索している場合
        if context['context'] == "medical":
            # contextに位置情報が含まれている場合
            if "location" in context:
                department = context['department']
                location = context['location']
                response = await find_nearby_medical_facilities(user_message, department, location) # user_messageは不要かも、引数は位置情報と診療科で十分。
                del user_context[user_id]
            # contextに位置情報が含まれていない場合
            else:
                response = "位置情報を送信してください。"

        # 薬剤情報の検索をしている場合
        elif context['context'] == "drug_info":
            # 引数にuser_messageを渡して、get_drug_infoを呼び出す
            response = await get_drug_info(user_message)
            # 薬剤情報検索の一連の処理が終わったら、contextからuser_idを削除し、trackingを終了する
            # ここで、「疑問は解決できましたか？」 - 「はい/いいえ」 で処理を終わるかどうかを決めてもいいかも。
            del user_context[user_id]

        # 医療機関検索でも薬剤検索でもないリクエストが送られてきた場合
        else:
            response = "すみません、理解できませんでした"

        # line_botのリプ: 上記の条件ごとに定義されたresponse_messageを返す
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response)
        )
    # contextにuser_idが含まれていない場合
    else:
        # テンプレメッセージ回答用のボタン定義
        buttons_template = ButtonsTemplate(
            title="選択してください",
            text="お役に立てることはありますか？",
            actions=[
                PostbackAction(label="医療機関を知りたい", data="medical"),
                PostbackAction(label="薬について聞きたい", data="drug_info")
            ]
        )

        # 上記で定義したボタンを保持したテンプレメッセージ
        template_message = TemplateSendMessage(
            alt_text="選択してください",
            template=buttons_template
        )

        # テンプレメッセージをユーザーに表示
        line_bot_api.reply_message(
            event.reply_token,
            template_message
        )

    # 取得できたuser_idとmessageをコンソール出力
    print(f"user_id: {user_id}")
    print(f"メッセージ: {user_message}")

# 医療機関の検索をする時の'department'の情報獲得用の処理: 獲得したらcontextへ追加される
@handler.add(PostbackEvent)
async def handle_postback(event):
    postback_data = event.postback.data
    user_id = event.source.user_id

    if postback_data == "medical":
        reply_message = "何科の受診をご希望ですか？"
        user_context[user_id] = {"context": "medical"}
        buttons_template = ButtonsTemplate(
            title="受診したい診療科を選択してください",
            text="以下の診療科から選択してください",
            actions=[
                PostbackAction(label="内科", data="department_internal_medicine"),
                PostbackAction(label="整形外科", data="department_orthopedics"),
                PostbackAction(label="泌尿器科", data="department_urology"),
                PostbackAction(label="婦人科", data="department_gynecology"),
                PostbackAction(label="耳鼻科", data="department_ent"),
                PostbackAction(label="皮膚科", data="department_dermatology"),
                PostbackAction(label="眼科", data="department_ophthalmology"),
                PostbackAction(label="精神科", data="department_psychiatry")
            ]
        )

        template_message = TemplateSendMessage(
            alt_text="診療科を選択してください",
            template=buttons_template
        )
        line_bot_api.reply_message(
            event.reply_token,
            template_message
        )

    elif postback_data == "drug_info":
        reply_message = "何というお薬の、どのようなことについてお調べしますか？"
        user_context[user_id] = {"context": "drug_info"}
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )
    
    elif "department_" in postback_data:
        department_mapping = {
            "department_internal_medicine": "内科",
            "department_orthopedics": "整形外科",
            "department_urology": "泌尿器科",
            "department_gynecology": "婦人科",
            "department_ent": "耳鼻科",
            "department_dermatology": "皮膚科",
            "department_ophthalmology": "眼科",
            "department_psychiatry": "精神科"
        }
        department = department_mapping.get(postback_data)
        user_context[user_id]['department'] = department
        reply_message = f"{department}の医療機関を検索するために、位置情報を送信してください。"
        location_message = LocationSendMessage(
            title="現在地を送信",
            address="タップして現在地を送信してください",
            latitude=0.0,
            longitude=0.0
        )
        line_bot_api.reply_message(
            event.reply_token,
            [TextSendMessage(text=reply_message), location_message]
        )
    else:
        reply_message = "すみません、理解できませんでした。"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_message)
        )

    print(f"postback_data: {postback_data}")

# 医療機関情報検索の時の'location'の情報獲得用の処理: 獲得したらcontextへ追加される
@handler.add(MessageEvent, message=LocationMessage)
async def handle_location(event):
    user_id = event.source.user_id
    latitude = event.message.latitude
    longitude = event.message.longitude

    if user_id in user_context:
        user_context[user_id]['location'] = {'latitude': latitude, 'longitude': longitude}
        reply_message = "位置情報を受け取りました。検索を続けるためにもう一度メッセージを入力してください。"
    else:
        reply_message = "位置情報を受け付けました。"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )

    print(f"user_id: {user_id}")
    print(f"位置情報: {latitude}, {longitude}")