# essential libraries
import os
import pandas as pd
import numpy as np

# regular expression import
import re

# uni-code library
import unicodedata

# natural language toolkit library/modules
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords


def basic_clean(string):
    """
    This function takes in a string and
    returns the string normalized.
    """
    string = (
        unicodedata.normalize("NFKD", string)
        .encode("ascii", "ignore")
        .decode("utf-8", "ignore")
    )
    string = re.sub(r"[^\w\s]", "", string).lower()
    return string


def tokenize(string):
    """
    This function takes in a string and
    returns a tokenized string.
    """
    # Create tokenizer.
    tokenizer = nltk.tokenize.ToktokTokenizer()

    # Use tokenizer
    string = tokenizer.tokenize(string, return_str=True)

    return string


def stem(string):
    """
    This function takes in a string and
    returns a string with words stemmed.
    """
    # Create porter stemmer.
    ps = nltk.porter.PorterStemmer()

    # Use the stemmer to stem each word in the list of words we created by using split.
    stems = [ps.stem(word) for word in string.split()]

    # Join our lists of words into a string again and assign to a variable.
    string = " ".join(stems)

    return string


def lemmatize(string):
    """
    This function takes in string for and
    returns a string with words lemmatized.
    """
    # Create the lemmatizer.
    wnl = nltk.stem.WordNetLemmatizer()

    # Use the lemmatizer on each word in the list of words we created by using split.
    lemmas = [wnl.lemmatize(word) for word in string.split()]

    # Join our list of words into a string again and assign to a variable.
    string = " ".join(lemmas)

    return string


def remove_stopwords(string, extra_words=[], exclude_words=[]):
    """
    This function takes in a string, optional extra_words and exclude_words parameters
    with default empty lists and returns a string.
    """
    # Create stopword_list.
    stopword_list = set()
    for language in stopwords.fileids():
        stopword_list = stopword_list.union(set(stopwords.words(language)))

    # Remove 'exclude_words' from stopword_list to keep these in my text.
    stopword_list = stopword_list - set(exclude_words)

    # Add in 'extra_words' to stopword_list.
    stopword_list = stopword_list.union(set(extra_words))

    # Split words in string.
    words = string.split()

    # Create a list of words from my string with stopwords removed and assign to variable.
    filtered_words = [word for word in words if word not in stopword_list]

    # Join words in the list back into strings and assign to a variable.
    string_without_stopwords = " ".join(filtered_words)

    return string_without_stopwords


def clean(text):
    """
    This function combines the above steps and added extra stop words to clean text
    """
    return remove_stopwords(lemmatize(basic_clean(text)))


import json
from collections import defaultdict, Counter
import matplotlib.colors as mcolors

with open("sentiment_output.json") as f:
    posts = json.load(f)


sentiment_colors = {
    "positive": np.array(mcolors.to_rgb("green")),
    "negative": np.array(mcolors.to_rgb("red")),
    "neutral": np.array(mcolors.to_rgb("gray")),
}

print("cleaning text...", end="\r")
sentiment_text = defaultdict(str)
for post in posts:
    for comment in post["comments"]:
        if comment["sentiment"] not in sentiment_colors:
            continue
        if comment["sentiment"] not in sentiment_text:
            sentiment_text[comment["sentiment"]] = ""
        sentiment_text[comment["sentiment"]] += comment["text"] + " "
for sentiment in sentiment_text:
    sentiment_text[sentiment] = clean(sentiment_text[sentiment])

sentiment_word_frequencies = {
    sentiment: Counter(text.split()) for sentiment, text in sentiment_text.items()
}
all_frequencies = sum(
    (Counter(freq) for freq in sentiment_word_frequencies.values()), Counter()
)


def sentiment_color_func(
    word, font_size, position, orientation, random_state=None, **kwargs
):
    total_occurrences = sum(
        sentiment_word_frequencies[sentiment][word]
        for sentiment in sentiment_word_frequencies
    )

    # Initialize color components
    blended_color = np.zeros(3)

    # Blend the colors based on the proportion of occurrences in each sentiment
    for sentiment, frequencies in sentiment_word_frequencies.items():
        proportion = frequencies[word] / total_occurrences
        blended_color += proportion * sentiment_colors[sentiment]

    # Convert the blended color back to a hex color code
    blended_color_hex = mcolors.to_hex(blended_color)

    return blended_color_hex


print("cleaning text... done")

# Create mask from jpg black/white image
from PIL import Image

ball_mask = np.array(Image.open("word_cloud/ball_mask.jpg"))

from wordcloud import WordCloud

img = WordCloud(
    background_color="white",
    width=4096,
    height=4096,
    mask=ball_mask,
    contour_color="black",
    contour_width=1,
).generate_from_frequencies(all_frequencies)
img.recolor(color_func=sentiment_color_func)

img.to_file("word_cloud/wordcloud.png")
