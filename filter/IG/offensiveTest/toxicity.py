import json
import requests
import csv
import time
import pandas as pd

def get_sources(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    sources = {item['source'] for item in data if item['source'].startswith('verovolley')}
    return list(sources)

def analyze_comment(api_key, comment):
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    data = {
        'comment': {'text': comment},
        'languages': ['it','en'],
        'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}, 'IDENTITY_ATTACK': {}, 'INSULT': {}}
    }
    response = requests.post(url, params={'key': api_key}, json=data)
    return response.json()

def add_toxicity_to_comments(file_path, api_key, source):
    with open(file_path, 'r') as f:
        data = json.load(f)

    csv_file_path = f'filter/IG/offensiveTest/{source}_comments_with_toxicity.csv'

    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['text', 'toxicity', 'severe_toxicity', 'identity_attack', 'insult', 'total_toxicity']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for item in data:
            if item['source'].startswith('verovolley'):
                for comment in item['comments']:
                    if comment['sentiment'] == 'negative' and 'toxicity' not in comment:
                        analysis = analyze_comment(api_key, comment['text'])
                        comment['toxicity'] = analysis['attributeScores']['TOXICITY']['summaryScore']['value']
                        comment['severe_toxicity'] = analysis['attributeScores']['SEVERE_TOXICITY']['summaryScore']['value']
                        comment['identity_attack'] = analysis['attributeScores']['IDENTITY_ATTACK']['summaryScore']['value']
                        comment['insult'] = analysis['attributeScores']['INSULT']['summaryScore']['value']
                        writer.writerow({'text': comment['text'], 'toxicity': comment['toxicity'], 'severe_toxicity': comment['severe_toxicity'], 'identity_attack': comment['identity_attack'], 'insult': comment['insult'], 'total_toxicity': comment['toxicity'] + comment['severe_toxicity'] + comment['identity_attack'] + comment['insult']})
                        # time.sleep(1) # necessario perchè possiamo fare solo 60 richieste al minuto ;)
                       

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
    sort_csv_by_total_toxicity(csv_file_path)

def sort_csv_by_total_toxicity(csv_file_path):
    df = pd.read_csv(csv_file_path)
    df = df.sort_values(by='total_toxicity', ascending=False)
    df.to_csv(csv_file_path, index=False)

def main():
    api_key = 'AIzaSyAbT4Axv-x3FJ18SBNsgCJHov0NAEdZjZY' # API key di Google Cloud Platform (sarebbe da nascondere)
    
    
    file_path = 'filter/IG/offensiveTest/sentiment_output.json'
    sources = get_sources(file_path)
    print(sources)
    for source in sources:
        add_toxicity_to_comments(file_path, api_key, source)
    

if __name__ == "__main__":
    main()