# import openai
# import asyncio

# openai.api_key = "YOUR_OPENAI_API_KEY"

# # ユーザーの入力を受け取る（例としてハードコード）
# drug_name = "アセトアミノフェン"
# info_type = "副作用"
# pmda_url = "https://www.pmda.go.jp/PmdaSearch/iyakuSearch/GeneralList?keyword=アセトアミノフェン"

# def generate_prompt(drug_name: str, info_type: str, pmda_url: str) -> str:
#     return f"薬剤名: {drug_name}\n知りたい情報: {info_type}\n以下のPMDAのURLから得られる情報を参考にして、薬についてユーザーにわかりやすい説明をしてください。\nURL: {pmda_url}"

# def generate_natural_language_response(prompt: str, model: str = "text-davinci-003") -> str:
#     response = openai.Completion.create(
#         engine=model,
#         prompt=prompt,
#         max_tokens=150
#     )
#     return response.choices[0].text.strip()

# async def get_drug_info(drug_name: str, info_type: str, pmda_url: str, model: str = "text-davinci-003") -> str:
#     prompt = generate_prompt(drug_name, info_type, pmda_url)
#     response = generate_natural_language_response(prompt, model)
#     return response

# # テストコード
# def test_generate_prompt():
#     expected_prompt = (
#         f"薬剤名: {drug_name}\n"
#         f"知りたい情報: {info_type}\n"
#         f"以下のPMDAのURLから得られる情報を参考にして、薬についてユーザーにわかりやすい説明をしてください。\n"
#         f"URL: {pmda_url}"
#     )
#     actual_prompt = generate_prompt(drug_name, info_type, pmda_url)
#     assert expected_prompt == actual_prompt, f"Expected: {expected_prompt}, but got: {actual_prompt}"

# def test_generate_natural_language_response():
#     prompt = generate_prompt(drug_name, info_type, pmda_url)
#     response = generate_natural_language_response(prompt)
#     assert isinstance(response, str) and len(response) > 0, "The response should be a non-empty string."

# async def test_get_drug_info():
#     response = await get_drug_info(drug_name, info_type, pmda_url, model="gpt-4")
#     assert isinstance(response, str) and len(response) > 0, "The final response should be a non-empty string."
#     print("Final Response:", response)

# # テスト関数を実行
# if __name__ == "__main__":
#     test_generate_prompt()
#     test_generate_natural_language_response()
#     asyncio.run(test_get_drug_info())


# import openai
# import asyncio

# # APIキーを設定
# openai.api_key = "YOUR_API_KEY"

# def generate_prompt(drug_name: str, info_type: str, pmda_url: str) -> str:
#     return (f"薬剤名: {drug_name}\n"
#             f"知りたい情報: {info_type}\n"
#             f"以下のPMDAのURLから得られる情報を参考にして、薬についてユーザーにわかりやすい説明をしてください。\n"
#             f"URL: {pmda_url}")

# def generate_natural_language_response(prompt: str, model: str = "gpt-4") -> str:
#     response = openai.ChatCompletion.create(
#         model=model,
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": prompt}
#         ],
#         max_tokens=150
#     )
#     return response.choices[0].message['content'].strip()

# async def get_drug_info(drug_name: str, info_type: str, pmda_url: str, model: str = "gpt-4") -> str:
#     prompt = generate_prompt(drug_name, info_type, pmda_url)
#     response = generate_natural_language_response(prompt, model)
#     return response

# # テストコード
# def test_generate_prompt():
#     expected_prompt = (
#         f"薬剤名: {drug_name}\n"
#         f"知りたい情報: {info_type}\n"
#         f"以下のPMDAのURLから得られる情報を参考にして、薬についてユーザーにわかりやすい説明をしてください。\n"
#         f"URL: {pmda_url}"
#     )
#     actual_prompt = generate_prompt(drug_name, info_type, pmda_url)
#     assert expected_prompt == actual_prompt, f"Expected: {expected_prompt}, but got: {actual_prompt}"

# def test_generate_natural_language_response():
#     prompt = generate_prompt(drug_name, info_type, pmda_url)
#     response = generate_natural_language_response(prompt)
#     assert isinstance(response, str) and len(response) > 0, "The response should be a non-empty string."

# async def test_get_drug_info():
#     response = await get_drug_info(drug_name, info_type, pmda_url, model="gpt-4")
#     assert isinstance(response, str) and len(response) > 0, "The final response should be a non-empty string."
#     print("Final Response:", response)

# # テスト関数を実行
# if __name__ == "__main__":
#     test_generate_prompt()
#     test_generate_natural_language_response()
#     asyncio.run(test_get_drug_info())

# import openai
# import asyncio

# # APIキーを設定
# openai.api_key = "YOUR_API_KEY"

# # グローバル変数の定義
# drug_name = "アセトアミノフェン"
# info_type = "副作用"
# pmda_url = "https://www.pmda.go.jp/PmdaSearch/iyakuSearch/GeneralList?keyword=アセトアミノフェン"

# def generate_prompt(drug_name: str, info_type: str, pmda_url: str) -> str:
#     return (f"薬剤名: {drug_name}\n"
#             f"知りたい情報: {info_type}\n"
#             f"以下のPMDAのURLから得られる情報を参考にして、薬についてユーザーにわかりやすい説明をしてください。\n"
#             f"URL: {pmda_url}")

# def generate_natural_language_response(prompt: str, model: str = "gpt-4") -> str:
#     response = openai.ChatCompletion.create(
#         model=model,
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": prompt}
#         ],
#         max_tokens=150
#     )
#     return response.choices[0].message['content'].strip()

# async def get_drug_info(drug_name: str, info_type: str, pmda_url: str, model: str = "gpt-4") -> str:
#     prompt = generate_prompt(drug_name, info_type, pmda_url)
#     response = generate_natural_language_response(prompt, model)
#     return response

# # テストコード
# def test_generate_prompt():
#     expected_prompt = (
#         f"薬剤名: {drug_name}\n"
#         f"知りたい情報: {info_type}\n"
#         f"以下のPMDAのURLから得られる情報を参考にして、薬についてユーザーにわかりやすい説明をしてください。\n"
#         f"URL: {pmda_url}"
#     )
#     actual_prompt = generate_prompt(drug_name, info_type, pmda_url)
#     assert expected_prompt == actual_prompt, f"Expected: {expected_prompt}, but got: {actual_prompt}"

# def test_generate_natural_language_response():
#     prompt = generate_prompt(drug_name, info_type, pmda_url)
#     response = generate_natural_language_response(prompt)
#     assert isinstance(response, str) and len(response) > 0, "The response should be a non-empty string."

# async def test_get_drug_info():
#     response = await get_drug_info(drug_name, info_type, pmda_url, model="gpt-4")
#     assert isinstance(response, str) and len(response) > 0, "The final response should be a non-empty string."
#     print("Final Response:", response)

# # テスト関数を実行
# if __name__ == "__main__":
#     test_generate_prompt()
#     test_generate_natural_language_response()
#     asyncio.run(test_get_drug_info())
# import openai
# import asyncio

# # APIキーを設定
# openai.api_key = "YOUR_API_KEY"

# # グローバル変数の定義
# drug_name = "アセトアミノフェン"
# info_type = "副作用"
# pmda_url = "https://www.pmda.go.jp/PmdaSearch/iyakuSearch/GeneralList?keyword=アセトアミノフェン"

# def generate_prompt(drug_name: str, info_type: str, pmda_url: str) -> str:
#     return (f"薬剤名: {drug_name}\n"
#             f"知りたい情報: {info_type}\n"
#             f"以下のPMDAのURLから得られる情報を参考にして、薬についてユーザーにわかりやすい説明をしてください。\n"
#             f"URL: {pmda_url}")

# async def generate_natural_language_response(prompt: str, model: str = "gpt-4") -> str:
#     response = await openai.ChatCompletion.acreate(
#         model=model,
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": prompt}
#         ],
#         max_tokens=150
#     )
#     return response.choices[0].message['content'].strip()

# async def get_drug_info(drug_name: str, info_type: str, pmda_url: str, model: str = "gpt-4") -> str:
#     prompt = generate_prompt(drug_name, info_type, pmda_url)
#     response = await generate_natural_language_response(prompt, model)
#     return response

# # テストコード
# def test_generate_prompt():
#     expected_prompt = (
#         f"薬剤名: {drug_name}\n"
#         f"知りたい情報: {info_type}\n"
#         f"以下のPMDAのURLから得られる情報を参考にして、薬についてユーザーにわかりやすい説明をしてください。\n"
#         f"URL: {pmda_url}"
#     )
#     actual_prompt = generate_prompt(drug_name, info_type, pmda_url)
#     assert expected_prompt == actual_prompt, f"Expected: {expected_prompt}, but got: {actual_prompt}"

# def test_generate_natural_language_response():
#     prompt = generate_prompt(drug_name, info_type, pmda_url)
#     response = asyncio.run(generate_natural_language_response(prompt))
#     assert isinstance(response, str) and len(response) > 0, "The response should be a non-empty string."

# async def test_get_drug_info():
#     response = await get_drug_info(drug_name, info_type, pmda_url, model="gpt-4")
#     assert isinstance(response, str) and len(response) > 0, "The final response should be a non-empty string."
#     print("Final Response:", response)

# # テスト関数を実行
# if __name__ == "__main__":
#     test_generate_prompt()
#     test_generate_natural_language_response()
#     asyncio.run(test_get_drug_info())


from openai import OpenAI, AsyncOpenAI
import os
import asyncio

# APIキーを設定
api_key = os.getenv("OPENAI_API_KEY")

# グローバル変数の定義
drug_name = "アセトアミノフェン"
info_type = "副作用"
pmda_url = "https://www.pmda.go.jp/PmdaSearch/iyakuSearch/GeneralList?keyword=アセトアミノフェン"

# generate_prompt: 薬剤名と知りたい情報、PMDAのURLを用いて、OpenAI GPTに与えるプロンプトを生成する
def generate_prompt(drug_name: str, info_type: str, pmda_url: str) -> str:
    return (f"薬剤名: {drug_name}\n"
            f"知りたい情報: {info_type}\n"
            f"以下のPMDAのURLから得られる情報を参考にして、薬についてユーザーにわかりやすい説明をしてください。\n"
            f"URL: {pmda_url}")
# generate_natural_language_response: 指定したプロンプトを基に、OpenAI GPTからのレスポンスを非同期に取得し、自然言語の回答を得る
async def generate_natural_language_response(prompt: str, model: str = "gpt-4") -> str:
    client = AsyncOpenAI(api_key=api_key)
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
# 修正: ドット記法で属性にアクセス
    return response.choices[0].message.content.strip() 
# get_drug_info: 薬剤名や情報の種類、PMDAのURLを基に、GPTからの回答を取得する
async def get_drug_info(drug_name: str, info_type: str, pmda_url: str, model: str = "gpt-4") -> str:
    prompt = generate_prompt(drug_name, info_type, pmda_url)
    response = await generate_natural_language_response(prompt, model)
    return response

# テストコード
# test_generate_prompt: generate_prompt 関数が正しいプロンプトを生成しているか確認する。期待されるプロンプトと実際に生成されたプロンプトを比較し、一致するか検証する。
def test_generate_prompt():
    expected_prompt = (
        f"薬剤名: {drug_name}\n"
        f"知りたい情報: {info_type}\n"
        f"以下のPMDAのURLから得られる情報を参考にして、薬についてユーザーにわかりやすい説明をしてください。\n"
        f"URL: {pmda_url}"
    )
    actual_prompt = generate_prompt(drug_name, info_type, pmda_url)
    assert expected_prompt == actual_prompt, f"Expected: {expected_prompt}, but got: {actual_prompt}"
# test_generate_natural_language_response: generate_natural_language_response 関数が、非同期で有効な文字列のレスポンスを返すか確認する。レスポンスが非空文字列であることをチェックする。
def test_generate_natural_language_response():
    prompt = generate_prompt(drug_name, info_type, pmda_url)
    response = asyncio.run(generate_natural_language_response(prompt))
    assert isinstance(response, str) and len(response) > 0, "The response should be a non-empty string."
# test_get_drug_info: get_drug_info 関数が、指定した薬剤情報を基に、有効な非空文字列のレスポンスを返すか確認する。また、最終的なレスポンスを出力する。
async def test_get_drug_info():
    response = await get_drug_info(drug_name, info_type, pmda_url, model="gpt-4")
    assert isinstance(response, str) and len(response) > 0, "The final response should be a non-empty string."
    print("Final Response:", response)

# テスト関数を実行
if __name__ == "__main__":
    test_generate_prompt()
    test_generate_natural_language_response()
    asyncio.run(test_get_drug_info())
