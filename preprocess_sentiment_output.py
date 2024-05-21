import json

from official_statistics.sentiment_total import process_post

with open("sentiment_output_with_offensives.json", "r") as f:
    posts = json.load(f)


source_to_keyword = {
    "paolaegonu_post": "egonu",
    "verovolley_alessiaorro8_post_comments_filtered.json": "orro",
    "verovolley_post_comments_filtered.json": "verovolley",
    "verovolley_miriamsylla_post_comments_filtered.json": "sylla",
    "miriamsylla_post": "sylla",
    "verovolley_crawl": "verovolley",
    "verovolley_paolaegonu_post_comments_filtered.json": "egonu",
}

for post in posts:
    if post["source"] in source_to_keyword:
        keyword = source_to_keyword[post["source"]]
        post["keywords"].append(keyword)

    post["keywords"] = list(set(post["keywords"]))


with open("Recharts/src/data/sentiment_output.json", "w") as f:
    json.dump([process_post(post) for post in posts], f, indent=2)
