import serpapi

params = {
  "engine": "google_lens",
  "url": "https://cdn.veritas-a.com/news/photo/old/4/3_1165480082.jpg",
  "api_key": '' #add your api
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