import openai
import asyncio

openai.api_key = "YOUR_OPENAI_API_KEY"

# ユーザーの入力を受け取る（例としてハードコード）
drug_name = "アセトアミノフェン"
info_type = "副作用"
pmda_url = "https://www.pmda.go.jp/PmdaSearch/iyakuSearch/GeneralList?keyword=アセトアミノフェン"

def generate_prompt(drug_name: str, info_type: str, pmda_url: str) -> str:
    return f"薬剤名: {drug_name}\n知りたい情報: {info_type}\n以下のPMDAのURLから得られる情報を参考にして、薬についてユーザーにわかりやすい説明をしてください。\nURL: {pmda_url}"

def generate_natural_language_response(prompt: str, model: str = "text-davinci-003") -> str:
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

async def get_drug_info(drug_name: str, info_type: str, pmda_url: str, model: str = "text-davinci-003") -> str:
    prompt = generate_prompt(drug_name, info_type, pmda_url)
    response = generate_natural_language_response(prompt, model)
    return response

# テストコード
def test_generate_prompt():
    expected_prompt = (
        f"薬剤名: {drug_name}\n"
        f"知りたい情報: {info_type}\n"
        f"以下のPMDAのURLから得られる情報を参考にして、薬についてユーザーにわかりやすい説明をしてください。\n"
        f"URL: {pmda_url}"
    )
    actual_prompt = generate_prompt(drug_name, info_type, pmda_url)
    assert expected_prompt == actual_prompt, f"Expected: {expected_prompt}, but got: {actual_prompt}"

def test_generate_natural_language_response():
    prompt = generate_prompt(drug_name, info_type, pmda_url)
    response = generate_natural_language_response(prompt)
    assert isinstance(response, str) and len(response) > 0, "The response should be a non-empty string."

async def test_get_drug_info():
    response = await get_drug_info(drug_name, info_type, pmda_url, model="gpt-4")
    assert isinstance(response, str) and len(response) > 0, "The final response should be a non-empty string."
    print("Final Response:", response)

# テスト関数を実行
if __name__ == "__main__":
    test_generate_prompt()
    test_generate_natural_language_response()
    asyncio.run(test_get_drug_info())
