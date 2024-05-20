import json

from official_statistics.sentiment_total import process_post

with open("sentiment_output.json", "r") as f:
    posts = json.load(f)

with open("Recharts/src/data/sentiment_output.json", "w") as f:
    json.dump([process_post(post) for post in posts], f, indent=2)
