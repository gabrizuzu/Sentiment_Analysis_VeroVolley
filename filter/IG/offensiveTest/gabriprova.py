import json
import requests
import time

def analyze_comment(api_key, comment):
    url = 'https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze'
    data = {
        'comment': {'text': comment},
        'languages': ['it','en'],
        'requestedAttributes': {'TOXICITY': {}, 'SEVERE_TOXICITY': {}, 'IDENTITY_ATTACK': {}, 'INSULT': {}}
    }
    response = requests.post(url, params={'key': api_key}, json=data)
    return response.json()

def add_toxicity_to_comments(file_path, api_key):
    with open(file_path, 'r') as f:
        data = json.load(f)

    for item in data:
        if item['source'] == 'verovolley_miriamsylla':
            for comment in item['comments']:
                if comment['sentiment'] == 'negative':
                    analysis = analyze_comment(api_key, comment['text'])
                    comment['toxicity'] = analysis['attributeScores']['TOXICITY']['summaryScore']['value']
                    comment['severe_toxicity'] = analysis['attributeScores']['SEVERE_TOXICITY']['summaryScore']['value']
                    comment['identity_attack'] = analysis['attributeScores']['IDENTITY_ATTACK']['summaryScore']['value']
                    comment['insult'] = analysis['attributeScores']['INSULT']['summaryScore']['value']
                    time.sleep(1) # necessario perchè possiamo fare solo 60 richieste al minuto ;)
                    print(comment['text'])
                    print(comment['toxicity'])
                    print(comment['severe_toxicity'])
                    print(comment['identity_attack'])
                    print(comment['insult'])

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

api_key = 'AIzaSyAbT4Axv-x3FJ18SBNsgCJHov0NAEdZjZY'
file_path = 'filter/IG/offensiveTest/sentiment_output.json'
add_toxicity_to_comments(file_path, api_key)