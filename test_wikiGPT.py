#Method1 for searching art Using Wikipedia

import wikipediaapi
import dotenv
import os
import openai

dotenv.load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
#wikipedia search -> ChatGPT Prompting -> connect to our highscale model
openai.api_key = openai_api_key

wiki_wiki = wikipediaapi.Wikipedia(
    user_agent='MyProjectName (merlin@example.com)',
    language='ko',
    extract_format=wikipediaapi.ExtractFormat.WIKI)
page_py = wiki_wiki.page('별이 빛나는 밤')

#need decide the length of text & Prompting
wiki_content = page_py.text[:4000]
prompt = f"너는 이제 도슨트의 역할을 해야해. 해당 주어진 문장에 대해서 잘 인지한 생태로, 사람들에게 내용을 4단락으로 전달해야 하는 목적이 있어. 작가의 삶에 대한 얘기보다 작품자체에 주목하고 싶어. 작품을 설명하고 있는 문장만을 이용해서, 해당 특성에 따라서 4단락으로 나눠서 설명해줘:\n{wiki_content}"

messages=[
    {
        "role": "system",
        "content": prompt,
    }
]

# GPT call
response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=messages,
  max_tokens=1000,
  temperature=0.9,
)

# print result
print(response.choices[0].message['content'])