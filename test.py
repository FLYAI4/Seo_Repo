import serpapi

params = {
  "engine": "google_lens",
  "url": "https://cdn.veritas-a.com/news/photo/old/4/3_1165480082.jpg",
  "api_key": "5d0437d641862ea9363678c09de0ecc1f0109f6d86be69339d81239486365358"
}

search = serpapi.search(params)
results = search.as_dict()
visual_matches = results["video_results"]

sentence = ''
count = 0

for i in visual_matches:
    count += 1
    sentence += f"{str(count)}: + {i['title']}\n"

print(sentence)