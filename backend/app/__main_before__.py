# import os
# from dotenv import load_dotenv
# from fastapi import FastAPI, Request, HTTPException
# from fastapi.responses import PlainTextResponse
# from linebot.v3 import WebhookHandler
# from linebot.v3.exceptions import InvalidSignatureError
# from linebot.v3.messaging import (
#     Configuration,
#     ApiClient,
#     MessagingApi,
#     ReplyMessageRequest,
#     TextMessage,
#     QuickReply,
#     QuickReplyItem,
#     MessageAction,
#     LocationAction
# )
# from linebot.v3.webhooks import (
#     MessageEvent,
#     TextMessageContent,
#     PostbackEvent,
#     LocationMessageContent
# )
# from .services.medical_facility_service import find_nearby_medical_facilities
# from .services.drug_info_service import get_drug_info

# load_dotenv()

# app = FastAPI()

# # 例外処理の追加
# configuration = None
# handler = None

# try:
#     configuration = Configuration(access_token=os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
#     handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
#     line_bot_api = MessagingApi(ApiClient(configuration))
#     print (f"Configuration: {Configuration}")
#     print(f"handler: {handler}")
#     print(f"line_bot_api: {line_bot_api}")
# except Exception:
#     print(f"環境変数の読み込みに失敗しました: {Exception}")

# user_context = {}

# # サーバー起動確認用のコード
# @app.get("/")
# async def index():
#     return "Hello, HARUKA, KU-MIN, MEME"

# @app.post("/callback/")
# async def callback(request: Request):
#     signature = request.headers['X-Line-Signature']
#     body = await request.body()
#     try:
#         print(f"◆signature: {signature}")
#         print ("メッセージ受信")
#         print(f"◆body: {body.decode('utf-8')}")
#         print(f"◆Configuration: {Configuration}")
#         print(f"◆handler: {handler}")
#         print(f"◆line_bot_api: {line_bot_api}")
#         handler.handle(body.decode('utf-8'), signature)
#     except InvalidSignatureError:
#         return "Invalid signature. Please check your channel access token/channel secret.", 400
#     return 'OK', 200

# # # 実際の検索ロジックを含む関数を飛び出す処理: contextが揃っている場合
# @handler.add(MessageEvent, message=TextMessageContent)
# def handle_message(event: MessageEvent):
#     print("handle_message called") 
#     try:
#         user_id = event.source.user_id
#         user_message = event.message.text

#         print(f"user_id: {user_id}")
#         print(f"メッセージ: {user_message}")

#         quick_reply_buttons = [
#                 QuickReplyItem(action=MessageAction(label="医療機関を知りたい", text="医療機関を知りたい")),
#                 QuickReplyItem(action=MessageAction(label="薬について聞きたい", text="薬について聞きたい"))
#             ]

#         quick_reply = QuickReply(items=quick_reply_buttons)

#         departments = ["内科", "整形外科", "耳鼻科", "眼科", "皮膚科", "泌尿器科", "婦人科", "精神科"]

#         if user_message == "医療機関を知りたい":
#             response = "今から検索します。何科を受診したいですか？"

#             quick_reply_department = [
#                 QuickReplyItem(action=MessageAction(label="内科", text="内科")),
#                 QuickReplyItem(action=MessageAction(label="整形外科", text="整形外科")),
#                 QuickReplyItem(action=MessageAction(label="耳鼻科", text="耳鼻科")),
#                 QuickReplyItem(action=MessageAction(label="眼科", text="眼科")),
#                 QuickReplyItem(action=MessageAction(label="皮膚科", text="皮膚科")),
#                 QuickReplyItem(action=MessageAction(label="婦人科", text="婦人科")),
#                 QuickReplyItem(action=MessageAction(label="泌尿器科", text="泌尿器科")),
#                 QuickReplyItem(action=MessageAction(label="精神科", text="精神科")),
#             ]

#             quick_reply = QuickReply(items=quick_reply_department)

#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     reply_token=event.reply_token,
#                     messages=[TextMessage(text=response, quick_reply=quick_reply)]
#                 )
#             )

#         elif user_message in departments :
#             selected_department = user_message
#             response = f"{user_message}ですね。それではお近くの医療機関を検索しますので、位置情報を送信してください。"

#             # ここに位置情報をユーザーに送信させる処理を追加
#             # 位置情報取得ができた時、その情報を変数locationで保持し
#             # selected_departmentと一緒に medical_facility_service に渡す
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     event.reply_token,
#                     [
#                         messages=[TextMessage(text=response)],
#                         LocationSendMessage(
#                             title="現在地を送信",
#                             address="",
#                             latitude=0.0,
#                             longitude=0.0
#                         )
#                     ]
#                 )
#             )


#         elif user_message == "薬について聞きたい":
#             response = "何というお薬の、どのようなことについて知りたいですか？"
#             # response = get_drug_info(user_message)
#             # del user_context[user_id]
#         else:
#             line_bot_api.reply_message(
#                 ReplyMessageRequest(
#                     reply_token=event.reply_token,
#                     messages=[TextMessage(text="お役に立てることはありますか？", quick_reply=quick_reply)]
#                 )
#             )
        
#         line_bot_api.reply_message(
#             ReplyMessageRequest(
#                 reply_token=event.reply_token,
#                 messages=[TextMessage(text=response)]
#             )
#         )

#     except Exception:
#         print(f"An error occurred: {Exception}")
#         line_bot_api.reply_message(
#             ReplyMessageRequest(
#                 reply_token=event.reply_token,
#                 messages=[TextMessage(text="申し訳ありませんが、処理中にエラーが発生しました。")]
#             )
#         )


# # 医療機関の検索をする時の'department'の情報獲得用の処理: 獲得したらcontextへ追加される
# @handler.add(PostbackEvent)
# async def handle_postback(event):
#     postback_data = event.postback.data
#     user_id = event.source.user_id

#     if postback_data == "medical":
#         reply_message = "何科の受診をご希望ですか？"
#         user_context[user_id] = {"context": "medical"}
#         buttons_template = ButtonsTemplate(
#             title="受診したい診療科を選択してください",
#             text="以下の診療科から選択してください",
#             actions=[
#                 PostbackAction(label="内科", data="department_internal_medicine"),
#                 PostbackAction(label="整形外科", data="department_orthopedics"),
#                 PostbackAction(label="泌尿器科", data="department_urology"),
#                 PostbackAction(label="婦人科", data="department_gynecology"),
#                 PostbackAction(label="耳鼻科", data="department_ent"),
#                 PostbackAction(label="皮膚科", data="department_dermatology"),
#                 PostbackAction(label="眼科", data="department_ophthalmology"),
#                 PostbackAction(label="精神科", data="department_psychiatry")
#             ]
#         )

#         template_message = TemplateSendMessage(
#             alt_text="診療科を選択してください",
#             template=buttons_template
#         )
#         line_bot_api.reply_message(
#             event.reply_token,
#             template_message
#         )

#     elif postback_data == "drug_info":
#         reply_message = "何というお薬の、どのようなことについてお調べしますか？"
#         user_context[user_id] = {"context": "drug_info"}
#         line_bot_api.reply_message(
#             event.reply_token,
#             TextSendMessage(text=reply_message)
#         )
    
#     elif "department_" in postback_data:
#         department_mapping = {
#             "department_internal_medicine": "内科",
#             "department_orthopedics": "整形外科",
#             "department_urology": "泌尿器科",
#             "department_gynecology": "婦人科",
#             "department_ent": "耳鼻科",
#             "department_dermatology": "皮膚科",
#             "department_ophthalmology": "眼科",
#             "department_psychiatry": "精神科"
#         }
#         department = department_mapping.get(postback_data)
#         user_context[user_id]['department'] = department
#         reply_message = f"{department}の医療機関を検索するために、位置情報を送信してください。"
#         location_message = LocationSendMessage(
#             title="現在地を送信",
#             address="タップして現在地を送信してください",
#             latitude=0.0,
#             longitude=0.0
#         )
#         line_bot_api.reply_message(
#             event.reply_token,
#             [TextSendMessage(text=reply_message), location_message]
#         )
#     else:
#         reply_message = "すみません、理解できませんでした。"
#         line_bot_api.reply_message(
#             event.reply_token,
#             TextSendMessage(text=reply_message)
#         )

#     print(f"postback_data: {postback_data}")

# @handler.add(PostbackEvent)
# async def handle_postback(event: PostbackEvent):
#     postback_data = event.postback.data
#     user_id = event.source.user_id

#     if postback_data == "medical":
#         reply_message = "何科の受診をご希望ですか？"
#         user_context[user_id] = {"context": "medical"}
#         quick_reply_buttons = [
#             QuickReplyItem(action=MessageAction(label="内科", text="内科")),
#             QuickReplyItem(action=MessageAction(label="整形外科", text="整形外科")),
#             QuickReplyItem(action=MessageAction(label="泌尿器科", text="泌尿器科")),
#             QuickReplyItem(action=MessageAction(label="婦人科", text="婦人科")),
#             QuickReplyItem(action=MessageAction(label="耳鼻科", text="耳鼻科")),
#             QuickReplyItem(action=MessageAction(label="皮膚科", text="皮膚科")),
#             QuickReplyItem(action=MessageAction(label="眼科", text="眼科")),
#             QuickReplyItem(action=MessageAction(label="精神科", text="精神科"))
#         ]

#         quick_reply = QuickReply(items=quick_reply_buttons)

#         await line_bot_api.reply_message(
#             ReplyMessageRequest(
#                 reply_token=event.reply_token,
#                 messages=[TextMessage(text=reply_message, quick_reply=quick_reply)]
#             )
#         )

#     elif postback_data == "drug_info":
#         reply_message = "何というお薬の、どのようなことについてお調べしますか？"
#         user_context[user_id] = {"context": "drug_info"}
#         await line_bot_api.reply_message(
#             ReplyMessageRequest(
#                 reply_token=event.reply_token,
#                 messages=[TextMessage(text=reply_message)]
#             )
#         )
    
#     elif "department_" in postback_data:
#         department_mapping = {
#             "department_internal_medicine": "内科",
#             "department_orthopedics": "整形外科",
#             "department_urology": "泌尿器科",
#             "department_gynecology": "婦人科",
#             "department_ent": "耳鼻科",
#             "department_dermatology": "皮膚科",
#             "department_ophthalmology": "眼科",
#             "department_psychiatry": "精神科"
#         }
#         department = department_mapping.get(postback_data)
#         user_context[user_id]['department'] = department
#         reply_message = f"{department}の医療機関を検索するために、位置情報を送信してください。"
#         location_message = LocationMessage(
#             title="現在地を送信",
#             address="タップして現在地を送信してください",
#             latitude=0.0,
#             longitude=0.0
#         )
#         await line_bot_api.reply_message(
#             ReplyMessageRequest(
#                 reply_token=event.reply_token,
#                 messages=[TextMessage(text=reply_message), location_message]
#             )
#         )
#     else:
#         reply_message = "すみません、理解できませんでした。"
#         await line_bot_api.reply_message(
#             ReplyMessageRequest(
#                 reply_token=event.reply_token,
#                 messages=[TextMessage(text=reply_message)]
#             )
#         )

#     print(f"postback_data: {postback_data}")

# # 医療機関情報検索の時の'location'の情報獲得用の処理: 獲得したらcontextへ追加される
# @handler.add(MessageEvent, message=LocationMessageContent)
# async def handle_location(event):
#     user_id = event.source.user_id
#     latitude = event.message.latitude
#     longitude = event.message.longitude

#     if user_id in user_context:
#         user_context[user_id]['location'] = {'latitude': latitude, 'longitude': longitude}
#         reply_message = "位置情報を受け取りました。検索を続けるためにもう一度メッセージを入力してください。"
#     else:
#         reply_message = "位置情報を受け付けました。"
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text=reply_message)
#     )

#     print(f"user_id: {user_id}")
#     print(f"位置情報: {latitude}, {longitude}")
