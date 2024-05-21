import json

with open("sentiment_output.json") as f:
    posts = json.load(f)

with open("offensive.json") as f:
    offensive = json.load(f)


def post_to_hash(post):
    return f"{post.get('taken_at_date')}{post.get('date')}{post.get('title')}{post.get('content')}"


def comment_to_hash(post_hash, comment):
    return f"{post_hash}{comment.get('text')}{comment.get('author')}{comment.get('user')}{comment.get('username')}{comment.get('created_at_utc')}{comment.get('date')}"


elements = {}
for post_i, post in enumerate(posts):
    post_hash = post_to_hash(post)
    elements[post_hash] = post_i
    for comment_i, comment in enumerate(post.get("comments", [])):
        comment_hash = comment_to_hash(post_hash, comment)
        elements[comment_hash] = comment_i

attrs = ["toxicity", "severe_toxicity", "identity_attack", "insult"]
for post in offensive:
    post_hash = post_to_hash(post)
    if post_hash in elements and post["source"].startswith("verovolley"):
        post_i = elements[post_hash]
        for comment in post.get("comments", []):
            comment_hash = comment_to_hash(post_hash, comment)
            if comment_hash not in elements or comment["sentiment"] != "negative":
                continue
            for attr in attrs:
                posts[post_i]["comments"][elements[comment_hash]][attr] = comment[attr]
            if "isToxic" in comment:
                posts[post_i]["comments"][elements[comment_hash]]["isToxic"] = comment[
                    "isToxic"
                ]

with open("sentiment_output_with_offensives.json", "w") as f:
    json.dump(posts, f, indent=2)
