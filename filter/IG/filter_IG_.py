import json
import re
import os
import csv

def load_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def save_data(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def keyword_in_text(data, keywords):
    items_with_keywords = []
    for item in data:
        content = item.get('content')
        if content is not None:
            content = content.lower()
        else:
            content = None
        item_keywords = []
        for keyword in keywords:
            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            if content is not None and re.search(pattern, content):
                item_keywords.append(keyword)
        if item_keywords:
            item['keywords'] = item_keywords
            items_with_keywords.append(item)
    return items_with_keywords

def main():
    directory_path = 'filter/IG/data'
    output_directory = 'filter/IG/output'
    keywords = [
        "monza", 
        "egonu", 
        "verovolley",
        "orro",
        "danesi",
        "larson",
        "cazaute",
        "malual",
        "heyrman",
        "folie",
        "prandi",
        "pusic",
        "rettke",
        "bajema",
        "sylla",
        "daalderop",
        "candi",
        "castillo",
        "vero volley",
        "allianz milano",
    ]

        # Elenco di tutti i file nella directory
    files = os.listdir(directory_path)

    csv_file_path = os.path.join(output_directory, 'post_counts.csv')
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Scrittura dell'intestazione del file CSV
        writer.writerow(['nome_file', 'numero_post','numero_commenti'])

        for file_name in files:
            # Ignora le directory
            if os.path.isdir(os.path.join(directory_path, file_name)):
                continue

            # Ignora i file che non sono JSON
            if not file_name.endswith('.json'):
                continue

            file_path = os.path.join(directory_path, file_name)
            output_path = os.path.join(output_directory, file_name.rsplit('.', 1)[0] + '_filtered.json')

            data = load_data(file_path)
            cleaned_data = []
            for item in data:

                comments = item['comments']
                cleaned_post = {
                    'content': item['caption'],
                    'taken_at_date': item['posted_at'],
                    'comments_count': item['comments_count'],
                    'likes_count': item['likes_count'],
                    'comments' : [{'text': comment['text'], 'username': comment['user']['username'], 'created_at_utc': comment['created_at_utc'],'like_count': comment['like_count']}for comment in comments]
                    
                }
                cleaned_data.append(cleaned_post)

            # Se il nome del file contiene "verovolley", salva i dati senza filtraggio
            if 'verovolley' in file_name.lower():
                save_data(cleaned_data, output_path)
                print(f"Number of posts in {file_name}: {len(cleaned_data)}")
                total_comments = 0
                for item in cleaned_data:
                    total_comments += item['comments_count']
                writer.writerow([file_name, len(cleaned_data), total_comments])
            else:
                filtered_data = keyword_in_text(cleaned_data, keywords)
                save_data(filtered_data, output_path)
                print(f"Number of posts in {file_name}: {len(filtered_data)}")
                total_comments = 0
                for item in filtered_data:
                    total_comments += item['comments_count']
                writer.writerow([file_name, len(filtered_data),total_comments])

            


if __name__ == "__main__":
    main()