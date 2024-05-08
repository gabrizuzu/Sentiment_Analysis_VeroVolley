import json
import re
import os
import csv

def load_data(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def save_data(data, file_path):
    for item in data:
        if 'comments' in item:
            for comment in item['comments']:
                if 'body' in comment:
                    comment['text'] = comment.pop('body')
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def keyword_in_text(data, keywords):
    items_with_keywords = []
    for item in data:
        content = item['content'].lower()
        item_keywords = []
        for keyword in keywords:
            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            if re.search(pattern, content):
                item_keywords.append(keyword)
        if item_keywords:
            item['keywords'] = item_keywords
            items_with_keywords.append(item)
    return items_with_keywords

def main():
    directory_path = 'filter/FB/data'
    output_directory = 'filter/FB/output'
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
        # Se il nome del file contiene "verovolley", salva i dati senza filtraggio
        if 'verovolley' in file_name.lower():
            save_data(data, output_path)
            print(f"Number of posts in {file_name}: {len(data)}")
            

        else:
            filtered_data = keyword_in_text(data, keywords)
            save_data(filtered_data, output_path)
            print(f"Number of posts in {file_name}: {len(filtered_data)}")
            

    csv_file_path = os.path.join(output_directory, 'post_counts.csv')
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Scrittura dell'intestazione del file CSV
        writer.writerow(['nome_file', 'numero_post'])
   
        # Scrittura dei dati nel file CSV
        for file_name in files:
            if file_name.endswith('.json'):
                filtered_file_name = file_name.rsplit('.', 1)[0] + '_filtered.json'
                filtered_data = load_data(os.path.join(output_directory, filtered_file_name))
                writer.writerow([file_name, len(filtered_data)])




if __name__ == "__main__":
    main()