import json

def calculate_toxicity_trends(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    post_toxicity = {}
    
    for index, item in enumerate(data):
        top_toxic_comments = []
        total_toxicity = 0
        for comment in item['comments']:
            if 'toxicity' in comment:
                total_toxicity += comment['toxicity']
                top_toxic_comments.append((comment['text'], comment['toxicity']))
        
        top_toxic_comments.sort(key=lambda x: x[1], reverse=True)
        top_toxic_comments = top_toxic_comments[:3]
        post_toxicity[index] = (item['content'],total_toxicity, top_toxic_comments)
        

    sorted_posts = sorted(post_toxicity.items(), key=lambda x: x[1], reverse=True)


    for post in sorted_posts:
        if post[1][1] > 0:
            print(f"Post content: {post[1][0]}, Total Toxicity: {post[1][1]}")
            print("Top 3 toxic comments:")
            for comment in post[1][2]:
                print(f"Comment: {comment[0]}, Toxicity: {comment[1]}")

file_path = 'filter/IG/offensiveTest/sentiment_output.json'
calculate_toxicity_trends(file_path)