# from model import get_model, predict_json, model_llama

# # Get Model
# model_base = model_llama
# model, tokenizer = get_model(model_base["model"], model_base["name"])

# filename = "test.json"

# # Predict
# predict_json(filename, model, tokenizer)

import os
import json

# Crawl folders to find the files and posts
FILTER_FOLDER = "filter"


def post_to_hash(post):
    return f"{post.get('taken_at_date')}{post.get('date')}{post.get('title')}{post.get('content')}"


def remove_duplicates(posts):
    set_to_skip = set()

    new_posts = []
    for post in posts:
        if post_to_hash(post) not in set_to_skip:
            new_posts.append(post)
            set_to_skip.add(post_to_hash(post))
    return new_posts


def get_elements(folder):
    platform_to_separator = {"FB": "crawl", "IG": "post", "Web": "output"}
    elements_to_process = []

    platforms_folder = f"{FILTER_FOLDER}"
    if folder == "keyword_filtered":
        platforms_folder = f"{FILTER_FOLDER}/keyword_filtered"

    platforms = next(os.walk(platforms_folder))[1]
    for platform in platforms:
        if platform not in platform_to_separator:
            continue

        files_folder = f"{platforms_folder}/{platform}"
        if folder != "keyword_filtered":
            files_folder += f"/{folder}"

        folder_files = next(os.walk(files_folder))[2]
        folder_files = list(
            filter(lambda x: (x.split(".")[-1] == "json"), folder_files)
        )

        for filename in folder_files:
            try:
                with open(f"{files_folder}/{filename}", "r") as f:
                    data = json.load(f)
            except:
                continue
            for post in data:
                post["comments"] = post["comments"] if post.get("comments") else []
                comments = []
                for comment in post["comments"]:
                    comment["author"] = (
                        comment["author"] if comment.get("author") else ""
                    )
                    if "verovolley" not in comment.get("author"):
                        comments.append(comment)
                post["comments"] = comments
            elements_to_process.extend(data)

    if folder != "data":
        elements_to_process = remove_duplicates(elements_to_process)

    return elements_to_process


elements = get_elements("output")
comments = sum(map(lambda x: len(x["comments"]), elements))
print("Static Filter:")
print(" Posts:", len(elements))
print(" Comments:", comments)
print(" Total:", len(elements) + comments)

print()

elements = get_elements("keyword_filtered")
comments = sum(map(lambda x: len(x["comments"]), elements))
print("Dynamic Filter:")
print(" Posts:", len(elements))
print(" Comments:", comments)
print(" Total:", len(elements) + comments)

print()

elements = get_elements("data")
comments = sum(map(lambda x: len(x["comments"]), elements))
print("Initial Data:")
print(" Posts:", len(elements))
print(" Comments:", comments)
print(" Total:", len(elements) + comments)
