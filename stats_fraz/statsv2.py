import json
import matplotlib.pyplot as plt
import os

def load_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def count_sentiments_all(data):
    sentiments = {'positive': 0, 'negative': 0, 'neutral': 0}
    for item in data:
        if 'comments' in item:
            for comment in item['comments']:
                if 'sentiment' in comment:
                    sentiments[comment['sentiment']] += 1
    return sentiments

def count_sentiments(data):
    sentiments = {}
    for item in data:
        source = item['source']
        if source not in sentiments:
            sentiments[source] = {'positive': 0, 'negative': 0, 'neutral': 0}
        if 'comments' in item:
            for comment in item['comments']:
                if 'sentiment' in comment:
                    sentiments[source][comment['sentiment']] += 1
    return sentiments

def count_sentiments_all_web(data):
    sentiments = {'positive': 0, 'negative': 0, 'neutral': 0}
    for item in data:
        if 'sentiment' in item:
            sentiments[item['sentiment']] += 1
    return sentiments

def count_sentiments_web(data):
    sentiments = {}
    for item in data:
        source = item['source']
        if source not in sentiments:
            sentiments[source] = {'positive': 0, 'negative': 0, 'neutral': 0}
        if 'sentiment' in item:
            sentiments[source][item['sentiment']] += 1
    return sentiments

def create_labels_all(sentiments):
    total = sum(sentiments.values())
    labels = [f'{k} - {v} ({v/total:.1%})' for k, v in sentiments.items()]
    return labels

def create_labels(sentiments):
    labels = {}
    for source, sentiment_counts in sentiments.items():
        source_total = sum(sentiment_counts.values())
        if source_total == 0:
            labels[source] = [f'{k} - {v} (0%)' for k, v in sentiment_counts.items()]
        else:
            labels[source] = [f'{k} - {v} ({v/source_total:.1%})' for k, v in sentiment_counts.items()]
    return labels

def custom_autopct(pct, allvalues):
    absolute = int(round(pct / 100. * sum(allvalues)))
    return f"{absolute}\n({pct:.1f}%)"

def create_pie_chart(sentiments, labels, platform):
    colors = ['#20519F', '#e14547', '#A8D9F0']
    sizes = list(sentiments.values())
    if sum(sizes) == 0:
        print(f"No data for {platform} General Sentiment. Skipping pie chart.")
        return

    plt.figure(figsize=(6, 6))
    patches, texts, autotexts = plt.pie(sizes, colors=colors, startangle=90, autopct=lambda pct: custom_autopct(pct, sizes))

    for text in texts:
        text.set_visible(False)  # Hide the default labels
    for autotext in autotexts:
        autotext.set_color('black')  # Change the text color to white for better readability
        autotext.set_fontsize(20)  # Adjust the font size if needed
        autotext.set_fontweight('bold')  # Set the font weight to bold

    plt.axis('equal')
    plt.title(f'{platform} General Sentiment')
    plt.savefig(f'C:/Users/simon/Repos/VeroVolley-Group-2/stats_fraz/{platform}/grafici/general_sentiment_pie_chart.png')
    plt.close()

def create_pie_chart_source(sentiments, labels, source, platform):
    colors = ['#20519F', '#e14547', '#A8D9F0']
    sizes = list(sentiments.values())
    if sum(sizes) == 0:
        print(f"No data for source {source} in platform {platform}. Skipping pie chart.")
        return

    plt.figure(figsize=(6, 6))
    patches, texts, autotexts = plt.pie(sizes, colors=colors, startangle=90, autopct=lambda pct: custom_autopct(pct, sizes))

    for text in texts:
        text.set_visible(False)  # Hide the default labels
    for autotext in autotexts:
        autotext.set_color('black')  # Change the text color to white for better readability
        autotext.set_fontsize(20)  # Adjust the font size if needed
        autotext.set_fontweight('bold')  # Set the font weight to bold

    plt.axis('equal')
    plt.title(f'Sentiment of comments from {source}')
    plt.savefig(f'C:/Users/simon/Repos/VeroVolley-Group-2/stats_fraz/{platform}/grafici/{source}_sentiment_pie_chart.png')
    plt.close()

def main():
    platforms = ['FB', 'IG', 'Web']
    for platform in platforms:
        data = load_data(f'C:/Users/simon/Repos/VeroVolley-Group-2/filter/{platform}/model_output/sentiment_output.json')
         # creo il grafico con i sentiment di tutto il dataset della piattaforma
        if platform == 'Web':
            sentiments_all = count_sentiments_all_web(data)
        else: 
            sentiments_all = count_sentiments_all(data)

        labels = create_labels_all(sentiments_all)
        create_pie_chart(sentiments_all, labels, platform)
        # creo il grafico con i sentiment divisi per source
        if platform == 'Web':
            sentiments_by_source = count_sentiments_web(data)
        else:
            sentiments_by_source = count_sentiments(data)

        labels_by_source = create_labels(sentiments_by_source)
        for source in sentiments_by_source.keys():
            create_pie_chart_source(sentiments_by_source[source], labels_by_source[source], source, platform)

if __name__ == "__main__":
    main()
