#Method2 for searching art Using Wikipedia
#need prompting for getting a good thinking or opinion from the professor of art

import os
import openai
import requests
from pprint import pprint
import dotenv

dotenv.load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
bing_search_api_key = os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY']
bing_search_endpoint = os.environ['BING_SEARCH_V7_ENDPOINT'] + \
    "v7.0/search"


def search(query):
    # Construct a request
    mkt = 'en-US'
    params = {'q': query, 'mkt': mkt}
    headers = {'Ocp-Apim-Subscription-Key': bing_search_api_key}

    # Call the API
    try:
        response = requests.get(bing_search_endpoint,
                                headers=headers, params=params)
        response.raise_for_status()
        json = response.json()
        return json["webPages"]["value"]

        # print("\nJSON Response:\n")
        # pprint(response.json())
    except Exception as ex:
        raise ex


# Prompt the user for a question
question = input("What is your question? ")

# Send a query to the Bing search engine and retrieve the results
results = search(question)

results_prompts = [
    f"Source:\nTitle: {result['name']}\nURL: {result['url']}\nContent: {result['snippet']}" for result in results
]

prompt = "Use the following sources to answer the question:\n\n" + \
    "\n\n".join(results_prompts) + "\n\nQuestion: " + question + "\n\nAnswer:"

print(prompt)

messages=[
    {
        "role": "system",
        "content": prompt,
    }
]

# Check if there are any results
if results:
    # Use OpenAI's GPT-3 API to answer the question
    openai.api_key = openai_api_key
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Print the answer from OpenAI
    answer = response.choices[0].message['content']
    print(f"Answer: {answer}")
else:
    # Print an error message if there are no results
    print("Error: No results found for the given query.")
