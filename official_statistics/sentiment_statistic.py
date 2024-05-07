import json
import matplotlib.pyplot as plt

def load_data(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data

def count_sentiments(data, key='sentiment'):
    count_pos = 0
    count_neg = 0
    count_neu = 0
    for item in data:
        sentiment = item.get(key)
        if sentiment == 'positive':
            count_pos += 1
        elif sentiment == 'negative':
            count_neg += 1
        elif sentiment == 'neutral':
            count_neu += 1
    return count_pos, count_neg, count_neu

def plot_sentiments(count_pos, count_neg, count_neu, title):
    labels = ['Positive', 'Negative', 'Neutral']
    values = [count_pos, count_neg, count_neu]
    bars = plt.bar(labels, values, color=['green', 'red', 'blue'], width = 0.5)
    for bar, value in zip(bars, values):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), value, ha='center', va='bottom', fontsize=8, color='black', weight='bold')
    plt.xlabel('Type of sentiment', fontsize=10, weight='bold')
    plt.ylabel('Values', fontsize=10, weight='bold')
    plt.title(title, fontsize=14)
    plt.show()

def main():
    data = load_data('output.json')
    count_pos, count_neg, count_neu = count_sentiments(data)
    print('Sentiment positive: ', count_pos)
    print('Sentiment negative: ', count_neg)
    print('Sentiment neutral: ', count_neu)
    plot_sentiments(count_pos, count_neg, count_neu, 'SENTIMENTAL ANALYSIS STATISTICS - POSTS')

    count_pos, count_neg, count_neu = count_sentiments(data, key='comments')
    print('Sentiment positive: ', count_pos)
    print('Sentiment negative: ', count_neg)
    print('Sentiment neutral: ', count_neu)
    plot_sentiments(count_pos, count_neg, count_neu, 'SENTIMENTAL ANALYSIS STATISTICS - COMMENTS')

if __name__ == "__main__":
    main()