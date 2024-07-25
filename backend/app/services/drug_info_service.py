from openai import OpenAI
import os
import logging

# ロガーの設定
# 詳細な情報の表示: asctime（タイムスタンプ）、levelname（ログレベル）、message（メッセージ内容）など、ログメッセージの詳細な情報を含める
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# APIキーを設定
api_key = os.getenv("OPENAI_API_KEY")

# グローバル変数の定義
drug_name = "ロキソプロフェン"
info_type = "使い方"
pmda_url = "https://www.pmda.go.jp/PmdaSearch/iyakuSearch/"


# generate_prompt: 薬剤名と知りたい情報、PMDAのURLを用いて、OpenAI GPTに与えるプロンプトを生成する
def generate_prompt(drug_name: str, info_type: str, pmda_url: str) -> str:
    logger.debug(f"Generating prompt for drug: {drug_name}, info type: {info_type}")
    return (f"薬剤名: {drug_name}\n"
            f"知りたい情報: {info_type}\n"
            f"以下のPMDAのURLから得られる情報を参考にして、薬についてユーザーにわかりやすい説明をしてください。\n"
            f"URL: {pmda_url}")
# generate_natural_language_response: 指定したプロンプトを基に、OpenAI GPTからのレスポンスを非同期に取得し、自然言語の回答を得る
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
# 修正: ドット記法で属性にアクセス
    return response.choices[0].message.content.strip() 
    
# check_relevance: 応答が薬品に関連しているかどうかをチェックする
def check_relevance(response: str) -> str:
    logger.debug(f"Checking relevance of response: {response}")
    if "薬" in response or "副作用" or "使い方" in response:
        return response
    else:
        logger.warning("Response is not relevant to the drug")
        return "薬品以外の質問には回答できません。"

# get_drug_info: 薬剤名や情報の種類、PMDAのURLを基に、GPTからの回答を取得する
def get_drug_info(drug_name: str, info_type: str, pmda_url: str, model: str = "gpt-4") -> str:
    logger.info(f"Fetching drug information for: {drug_name}, info type: {info_type}")
    prompt = generate_prompt(drug_name, info_type, pmda_url)
    response = generate_natural_language_response(prompt, model)
    logger.debug(f"Final relevant response: {relevant_response}")
    return response

# # テストコード
# # test_generate_prompt: generate_prompt 関数が正しいプロンプトを生成しているか確認する。期待されるプロンプトと実際に生成されたプロンプトを比較し、一致するか検証する。
# def test_generate_prompt():
#     expected_prompt = (
#         f"薬剤名: {drug_name}\n"
#         f"知りたい情報: {info_type}\n"
#         f"以下のPMDAのURLから得られる情報を参考にして、薬についてユーザーにわかりやすい説明をしてください。\n"
#         f"URL: {pmda_url}"
#     )
#     actual_prompt = generate_prompt(drug_name, info_type, pmda_url)
#     assert expected_prompt == actual_prompt, f"Expected: {expected_prompt}, but got: {actual_prompt}"
# # test_generate_natural_language_response: generate_natural_language_response 関数が、非同期で有効な文字列のレスポンスを返すか確認する。レスポンスが非空文字列であることをチェックする。
# def test_generate_natural_language_response():
#     prompt = generate_prompt(drug_name, info_type, pmda_url)
#     response = asyncio.run(generate_natural_language_response(prompt))
#     assert isinstance(response, str) and len(response) > 0, "The response should be a non-empty string."
# # test_get_drug_info: get_drug_info 関数が、指定した薬剤情報を基に、有効な非空文字列のレスポンスを返すか確認する。また、最終的なレスポンスを出力する。
# async def test_get_drug_info():
#     response = await get_drug_info(drug_name, info_type, pmda_url, model="gpt-4")
#     assert isinstance(response, str) and len(response) > 0, "The final response should be a non-empty string."
#     print("Final Response:", response)

# # テスト関数を実行
# if __name__ == "__main__":
#     test_generate_prompt()
#     test_generate_natural_language_response()
#     asyncio.run(test_get_drug_info())











# ※（仮）プロンプトのみ追加挿入※
# from openai import OpenAI
# import os

# # APIキーを設定
# api_key = os.getenv("OPENAI_API_KEY")

# # グローバル変数の定義
# drug_name = "ロキソプロフェン"
# info_type = "使い方"
# pmda_url = "https://www.pmda.go.jp/PmdaSearch/iyakuSearch/"


# # generate_prompt: 薬剤名と知りたい情報、PMDAのURLを用いて、OpenAI GPTに与えるプロンプトを生成する
# def generate_prompt(drug_name: str, info_type: str, pmda_url: str) -> str:
#     return (f"薬剤名: {drug_name}\n"
#             f"知りたい情報: {info_type}\n"
#             f"以下のPMDAのURLから得られる情報を基に、薬について詳細かつわかりやすく説明してください。\n"
#             f"URL: {pmda_url}\n"
#             f"説明に含めるべき情報:\n"
#             f"- 使用方法: この薬の正しい使い方について説明してください。\n"
#             f"- 副作用: 可能な副作用やその対処法について説明してください。\n"
#             f"- 注意点: 使用時の注意点や禁忌事項について説明してください。\n"
#             f"- 推奨用量: 推奨される用量と使用頻度について説明してください。\n"
#             f"ユーザーがこの情報を基に適切に薬を使用できるように、具体的で実用的な説明をお願いします。")
# # generate_natural_language_response: 指定したプロンプトを基に、OpenAI GPTからのレスポンスを非同期に取得し、自然言語の回答を得る
# def generate_natural_language_response(prompt: str, model: str = "gpt-4") -> str:
#     client = OpenAI(api_key=api_key)
#     response = client.chat.completions.create(
#         model=model,
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": prompt}
#         ],
#         max_tokens=500,  # 最大500トークンまでの応答
#         temperature=0.5,  # 値が0に近いほど、モデルはより決定的な応答を生成
#         top_p=1  # すべてのトークンを考慮する
#     )
# # 修正: ドット記法で属性にアクセス
#     return response.choices[0].message.content.strip() 

# # check_relevance: 応答が薬品に関連しているかどうかをチェックする
# def check_relevance(response: str) -> str:
#     if "薬" in response or "副作用" or "使い方" in response:
#         return response
#     else:
#         return "薬品以外の質問には回答できません。"

# # get_drug_info: 薬剤名や情報の種類、PMDAのURLを基に、GPTからの回答を取得する
# def get_drug_info(drug_name: str, info_type: str, pmda_url: str, model: str = "gpt-4") -> str:
#     prompt = generate_prompt(drug_name, info_type, pmda_url)
#     response = generate_natural_language_response(prompt, model)
#     return response











# ※（仮）会話履歴取得する関数のみ挿入※
# from openai import OpenAI
# import os
# from sqlalchemy.orm import Session

# # APIキーを設定
# api_key = os.getenv("OPENAI_API_KEY")

# # グローバル変数の定義
# drug_name = "ロキソプロフェン"
# info_type = "使い方"
# pmda_url = "https://www.pmda.go.jp/PmdaSearch/iyakuSearch/"

# # データベースセッションの取得（仮の関数）
# def get_db_session() -> Session:
#     # データベースセッションを返す実装が必要
#     pass

# # 会話履歴を取得する関数
# def get_user_conversation_history(db: Session, user_id: str):
#     return db.query(ConversationHistory).filter(ConversationHistory.user_id == user_id).all()

# # プロンプトを生成する関数（会話履歴なし）
# def generate_prompt(drug_name: str, info_type: str, pmda_url: str) -> str:
#     return (f"薬剤名: {drug_name}\n"
#             f"知りたい情報: {info_type}\n"
#             f"以下のPMDAのURLから得られる情報を参考にして、薬についてユーザーにわかりやすい説明をしてください。\n"
#             f"URL: {pmda_url}")

# # 会話履歴を基にプロンプトを生成する関数
# def generate_prompt_with_history(drug_name: str, info_type: str, pmda_url: str, conversation_history: str) -> str:
#     return (f"ユーザーとの過去の会話:\n{conversation_history}\n"
#             f"薬剤名: {drug_name}\n"
#             f"知りたい情報: {info_type}\n"
#             f"以下のPMDAのURLから得られる情報を参考にして、薬についてユーザーにわかりやすい説明をしてください。\n"
#             f"URL: {pmda_url}")

# # 指定したプロンプトを基に、OpenAI GPTからのレスポンスを非同期に取得する関数
# def generate_natural_language_response(prompt: str, model: str = "gpt-4") -> str:
#     client = OpenAI(api_key=api_key)
#     response = client.chat.completions.create(
#         model=model,
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": prompt}
#         ],
#         max_tokens=500,  # 最大500トークンまでの応答
#         temperature=0.5,  # 値が0に近いほど、モデルはより決定的な応答を生成
#         top_p=1  # すべてのトークンを考慮する
#     )
#     return response.choices[0].message.content.strip()

# # 薬剤に関する情報を取得する関数
# def get_drug_info(drug_name: str, info_type: str, pmda_url: str, model: str = "gpt-4") -> str:
#     prompt = generate_prompt(drug_name, info_type, pmda_url)
#     response = generate_natural_language_response(prompt, model)
#     return response

# # 会話履歴を考慮して応答を生成する関数
# def generate_response_with_history(user_id: str, db: Session, drug_name: str, info_type: str, pmda_url: str, model: str = "gpt-4") -> str:
#     # ユーザーの会話履歴を取得
#     conversation_history = get_user_conversation_history(db, user_id)
    
#     # 会話履歴を整形
#     formatted_history = "\n".join([f"ユーザー: {conv.user_message}\nボット: {conv.bot_response}" for conv in conversation_history])
    
#     # 会話履歴を含むプロンプトを生成
#     prompt = generate_prompt_with_history(drug_name, info_type, pmda_url, formatted_history)
    
#     # 応答を生成
#     response = generate_natural_language_response(prompt, model)
    
#     return response

# # 使用例
# db_session = get_db_session()  # データベースセッションの取得（仮の関数）
# user_id = 'example_user_id'
# response = generate_response_with_history(user_id, db_session, drug_name, info_type, pmda_url)
# print(response)















# ※これが動くコードだよ※
# from openai import OpenAI
# import os

# # APIキーを設定
# api_key = os.getenv("OPENAI_API_KEY")

# # グローバル変数の定義
# drug_name = "ロキソプロフェン"
# info_type = "使い方"
# pmda_url = "https://www.pmda.go.jp/PmdaSearch/iyakuSearch/"


# # generate_prompt: 薬剤名と知りたい情報、PMDAのURLを用いて、OpenAI GPTに与えるプロンプトを生成する
# def generate_prompt(drug_name: str, info_type: str, pmda_url: str) -> str:
#     return (f"薬剤名: {drug_name}\n"
#             f"知りたい情報: {info_type}\n"
#             f"以下のPMDAのURLから得られる情報を参考にして、薬についてユーザーにわかりやすい説明をしてください。\n"
#             f"URL: {pmda_url}")
# # generate_natural_language_response: 指定したプロンプトを基に、OpenAI GPTからのレスポンスを非同期に取得し、自然言語の回答を得る
# def generate_natural_language_response(prompt: str, model: str = "gpt-4") -> str:
#     client = OpenAI(api_key=api_key)
#     response = client.chat.completions.create(
#         model=model,
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": prompt}
#         ],
#         max_tokens=500,  # 最大500トークンまでの応答
#         temperature=0.5,  # 値が0に近いほど、モデルはより決定的な応答を生成
#         top_p=1  # すべてのトークンを考慮する
#     )
# # 修正: ドット記法で属性にアクセス
#     return response.choices[0].message.content.strip() 

# # check_relevance: 応答が薬品に関連しているかどうかをチェックする
# def check_relevance(response: str) -> str:
#     if "薬" in response or "副作用" or "使い方" in response:
#         return response
#     else:
#         return "薬品以外の質問には回答できません。"

# # get_drug_info: 薬剤名や情報の種類、PMDAのURLを基に、GPTからの回答を取得する
# def get_drug_info(drug_name: str, info_type: str, pmda_url: str, model: str = "gpt-4") -> str:
#     prompt = generate_prompt(drug_name, info_type, pmda_url)
#     response = generate_natural_language_response(prompt, model)
#     return response

# # # テストコード
# # # test_generate_prompt: generate_prompt 関数が正しいプロンプトを生成しているか確認する。期待されるプロンプトと実際に生成されたプロンプトを比較し、一致するか検証する。
# # def test_generate_prompt():
# #     expected_prompt = (
# #         f"薬剤名: {drug_name}\n"
# #         f"知りたい情報: {info_type}\n"
# #         f"以下のPMDAのURLから得られる情報を参考にして、薬についてユーザーにわかりやすい説明をしてください。\n"
# #         f"URL: {pmda_url}"
# #     )
# #     actual_prompt = generate_prompt(drug_name, info_type, pmda_url)
# #     assert expected_prompt == actual_prompt, f"Expected: {expected_prompt}, but got: {actual_prompt}"
# # # test_generate_natural_language_response: generate_natural_language_response 関数が、非同期で有効な文字列のレスポンスを返すか確認する。レスポンスが非空文字列であることをチェックする。
# # def test_generate_natural_language_response():
# #     prompt = generate_prompt(drug_name, info_type, pmda_url)
# #     response = asyncio.run(generate_natural_language_response(prompt))
# #     assert isinstance(response, str) and len(response) > 0, "The response should be a non-empty string."
# # # test_get_drug_info: get_drug_info 関数が、指定した薬剤情報を基に、有効な非空文字列のレスポンスを返すか確認する。また、最終的なレスポンスを出力する。
# # async def test_get_drug_info():
# #     response = await get_drug_info(drug_name, info_type, pmda_url, model="gpt-4")
# #     assert isinstance(response, str) and len(response) > 0, "The final response should be a non-empty string."
# #     print("Final Response:", response)

# # # テスト関数を実行
# # if __name__ == "__main__":
# #     test_generate_prompt()
# #     test_generate_natural_language_response()
# #     asyncio.run(test_get_drug_info())
