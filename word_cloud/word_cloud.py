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

nltk.download("stopwords")
nltk.download("wordnet")


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


italianExcludewords = [
    "perche",
    "comunque",
    "quindi",
    "pero",
    "quindi",
    "pero",
    "per",
    "anche",
    "ancora",
    "quando",
    "dopo",
    "prima",
    "poi",
    "fino",
    "ora",
    "già",
    "appena",
    "mentre",
    "sempre",
    "tutto",
    "nulla",
    "tutti",
    "nessuno",
    "qualcosa",
    "qualcuno",
    "alcuni",
    "alcuno",
    "ogni",
    "nessuno",
    "alcun",
    "alcuna",
    "ognuno",
    "ognuna",
    "tanto",
    "troppo",
    "poco",
    "molto",
    "così",
    "cosi",
    "quanto",
    "quanti",
    "quanta",
    "quante",
    "tanto",
    "tanti",
    "tanta",
    "tante",
    "altro",
    "altra",
    "altri",
    "altre",
    "stesso",
    "stessa",
    "stessi",
    "stesse",
    "proprio",
    "propria",
    "propri",
    "proprie",
    "davvero",
    "veramente",
    "solo",
    "solamente",
    "soltanto",
    "pure",
    "anche",
    "addirittura",
    "perfino",
    "addirittura",
    "pure",
    "anche",
    "addirittura",
    "perfino",
    "soprattutto",
    "specialmente",
    "particolarmente",
    "soprattutto",
    "specialmente",
    "particolarmente",
    "quasi",
    "pressappoco",
    "circa",
    "approssimativamente",
    "quasi",
    "pressappoco",
    "circa",
    "approssimativamente",
    "piuttosto",
    "abbastanza",
    "assai",
    "per",
    "solo",
    "soltanto",
    "unicamente",
    "esclusivamente",
    "escluso",
    "eccetto",
    "tranne",
    "tutta",
    "tutte",
    "tutti",
    "tutto",
    "ogni",
    "ognuno",
    "ognuna",
    "ciascuno",
    "ciascuna",
    "ciascuno",
    "ciascuna",
    "alcuni",
    "alcune",
    "alcuni",
    "alcune",
    "qualche",
    "alcuni",
    "alcune",
    "alcuni",
    "alcune",
    "qualche",
    "altri",
    "altre",
    "altri",
    "altre",
    "quali",
    "quale",
    "quali",
    "quale",
    "quanto",
    "quanta",
    "quanti",
    "quante",
    "quanto",
    "quanta",
    "quanti",
    "quante",
    "quel",
    "quello",
    "quella",
    "quelli",
    "quelle",
    "quello",
    "quella",
    "quelli",
    "quelle",
    "questo",
    "questa",
    "questi",
    "queste",
    "questo",
    "questa",
    "questi",
    "queste",
    "stesso",
    "stessa",
    "stessi",
    "stesse",
    "stesso",
    "stessa",
    "stessi",
    "stesse",
    "medesimo",
    "medesima",
    "medesimi",
    "medesime",
    "medesimo",
    "medesima",
    "medesimi",
    "medesime",
    "proprio",
    "propria",
    "propri",
    "proprie",
    "proprio",
    "propria",
    "propri",
    "proprie",
    "cose",
    "cosa",
    "cose",
    "cosa",
    "fatto",
    "fatti",
    "fatta",
    "fatte",
    "fatto",
    "fatti",
    "fatta",
    "fatte",
    "volta",
    "volte",
    "volta",
    "volte",
    "tempo",
    "tempi",
    "tempo",
    "tempi",
    "modo",
    "modi",
    "modo",
    "modi",
    "parte",
    "parti",
    "parte",
    "parti",
    "luogo",
    "luoghi",
    "luogo",
    "luoghi",
    "persona",
    "persone",
    "persona",
    "persone",
    "cosa",
    "cose",
    "cosa",
    "cose",
    "ragione",
    "ragioni",
    "ragione",
    "ragioni",
    "motivo",
    "motivi",
    "motivo",
    "motivi",
    "scopo",
    "scopi",
    "scopo",
    "scopi",
    "mezzo",
    "mezzi",
    "mezzo",
    "mezzi",
    "fine",
    "fini",
    "fine",
    "fini",
    "modo",
    "modi",
    "modo",
    "modi",
    "ragione",
    "ragioni",
    "ragione",
    "ragioni",
    "motivo",
    "motivi",
    "motivo",
    "motivi",
    "piu",
    "più",
    "meno",
    "meno",
    "tanto",
    "tanto",
    "troppo",
    "troppo",
    "poco",
    "poco",
    "molto",
    "molto",
    "cosi",
    "così",
    "quasi",
    "quasi",
    "abbastanza",
    "abbastanza",
    "assai",
    "assai",
    "troppo",
    "troppo",
    "poco",
    "poco",
    "molto",
    "molto",
    "cosi",
    "così",
    "quasi",
    "quasi",
    "abbastanza",
    "abbastanza",
    "assai",
    "assai",
    "percha",
    "fare",
    "faccio",
    "faccia",
    "facciamo",
    "facciate",
    "facciano",
    "faccio",
    "fai",
    "faccia",
    "facciamo",
    "fate",
    "fanno",
    "farò",
    "farai",
    "farà",
    "faremo",
    "farete",
    "faranno",
    "farei",
    "faresti",
    "farebbe",
    "faresti",
    "farebbe",
    "faremmo",
    "fareste",
    "farebbero",
    "farei",
    "faresti",
    "farebbe",
    "faremmo",
    "fareste",
    "farebbero",
    "facessi",
    "facesse",
    "facessimo",
    "faceste",
    "facessero",
    "facessi",
    "facesse",
    "facessimo",
    "faceste",
    "facessero",
    "facessi",
    "facesse",
    "essere",
    "sono",
    "sia",
    "siamo",
    "siate",
    "siano",
    "essendo",
    "stato",
    "ero",
    "era",
    "eravamo",
    "eravate",
    "erano",
    "fui",
    "fuisti",
    "fu",
    "fummo",
    "foste",
    "furono",
    "fossi",
    "fosse",
    "fossimo",
    "foste",
    "fossero",
    "fossi",
    "fosse",
    "fossimo",
    "foste",
    "fossero",
    "essendo",
    "stato",
    "avere",
    "ho",
    "ha",
    "abbiamo",
    "avete",
    "hanno",
    "puo",
    "posso",
    "puoi",
    "puo",
    "possiamo",
    "potete",
    "possono",
    "potrei",
    "potresti",
    "potrebbe",
    "potremmo",
    "potreste",
    "potrebbero",
    "posso",
    "puoi",
    "puo",
    "possiamo",
    "potete",
    "possono",
    "potrei",
    "potresti",
    "potrebbe",
    "potremmo",
    "potreste",
    "potrebbero",
    "posso",
    "puoi",
    "puo",
    "possiamo",
    "potete",
    "possono",
    "potrei",
    "potresti",
    "potrebbe",
    "potremmo",
    "potreste",
    "potrebbero",
    "posso",
    "puoi",
    "puo",
    "possiamo",
    "potete",
    "possono",
    "potrei",
    "potresti",
    "potrebbe",
    "potremmo",
    "potreste",
    "potrebbero",
    "posso",
    "puoi",
    "puo",
    "possiamo",
    "potete",
    "possono",
    "potrei",
    "potresti",
    "potrebbe",
    "potremmo",
    "potreste",
    "potrebbero",
    "posso",
    "puoi",
    "puo",
    "possiamo",
    "potete",
    "possono",
    "potrei",
    "potresti",
    "potrebbe",
    "potremmo",
    "potreste",
    "potrebbero",
    "posso",
    "puoi",
    "semplicemente",
    "semplice",
    "semplicemente",
    "semplice",
    "solo",
    "soltanto",
    "unicamente",
    "esclusivamente",
    "escluso",
    "eccetto",
    "tranne",
    "tutta",
    "tutte",
    "gia",
    "pua",
    "invece",
    "niente",
    "nulla",
    "nessuno",
    "nessuna",
    "nessun",
    "nessuno",
    "nessuna",
    "nessun",
    "nulla",
    "natale",
    "ieri",
    "oggi",
    "domani",
    "dopo",
    "prima",
    "poi",
    "fino",
    "ora",
    "già",
    "appena",
    "mentre",
    "sempre",
    "tutto",
    "nulla",
    "tutti",
    "nessuno",
    "qualcosa",
    "qualcuno",
    "alcuni",
    "alcuno",
    "ogni",
    "nessuno",
    "alcun",
    "alcuna",
    "ognuno",
    "ognuna",
    "tanto",
    "troppo",
    "poco",
    "molto",
    "così",
    "cosi",
    "quanto",
    "quanti",
    "quanta",
    "quante",
    "tanto",
    "tanti",
    "tanta",
    "tante",
    "altro",
    "altra",
    "altri",
    "altre",
    "stesso",
    "stessa",
    "stessi",
    "stesse",
    "proprio",
    "propria",
    "propri",
    "proprie",
    "davvero",
    "veramente",
    "solo",
    "solamente",
    "soltanto",
    "pure",
    "anche",
    "addirittura",
    "perfino",
    "addirittura",
    "pure",
    "anche",
    "addirittura",
    "perfino",
    "soprattutto",
    "specialmente",
    "particolarmente",
    "soprattutto",
    "specialmente",
    "particolarmente",
    "quasi",
    "pressappoco",
    "circa",
    "approssimativamente",
    "quasi",
    "pressappoco",
    "circa",
    "approssimativamente",
    "piuttosto",
    "abbastanza",
    "assai",
    "per",
    "solo",
    "soltanto",
    "unicamente",
    "esclusivamente",
    "escluso",
    "eccetto",
    "tranne",
    "tutta",
    "tutte",
    "tutti",
    "tutto",
    "ogni",
    "ognuno",
    "ognuna",
    "ciascuno",
    "ciascuna",
    "ciascuno",
    "ciascuna",
    "alcuni",
    "alcune",
    "alcuni",
    "alcune",
    "qualche",
    "alcuni",
    "alcune",
    "alcuni",
    "alcune",
    "qualche",
    "altri",
    "altre",
    "altri",
    "altre",
    "quali",
    "quale",
    "quali",
    "quale",
    "quanto",
    "quanta",
    "quanti",
    "quante",
    "quanto",
    "quanta",
    "quanti",
    "quante",
    "quel",
    "quello",
    "quella",
    "quelli",
    "quelle",
    "quello",
    "quella",
    "quelli",
    "quelle",
    "questo",
    "questa",
    "questi",
    "queste",
    "questo",
    "questa",
    "questi",
    "queste",
    "stesso",
    "stessa",
    "stessi",
    "stesse",
    "stesso",
    "stessa",
    "stessi",
    "stesse",
    "medesimo",
    "medesima",
    "medesimi",
    "medesime",
    "medesimo",
    "medesima",
    "medesimi",
    "medesime",
    "proprio",
    "propria",
    "propri",
    "proprie",
    "proprio",
    "propria",
    "propri",
    "proprie",
    "cose",
    "cosa",
    "cose",
    "cosa",
    "fatto",
    "fatti",
    "fatta",
    "fatte",
    "fatto",
    "fatti",
    "fatta",
    "fatte",
    "volta",
    "volte",
    "volta",
    "volte",
    "tempo",
    "tempi",
    "tempo",
    "tempi",
    "modo",
    "modi",
    "modo",
    "modi",
    "parte",
    "parti",
    "parte",
    "parti",
    "luogo",
    "luoghi",
    "luogo",
    "luoghi",
    "persona",
    "persone",
    "persona",
    "persone",
    "cosa",
    "cose",
    "cosa",
    "cose",
    "ragione",
    "ragioni",
    "ragione",
    "ragioni",
    "motivo",
    "motivi",
    "motivo",
    "motivi",
    "scopo",
    "scopi",
    "scopo",
    "scopi",
    "mezzo",
    "mezzi",
    "mezzo",
    "mezzi",
    "fine",
    "fini",
    "fine",
    "fini",
    "modo",
    "modi",
    "modo",
    "modi",
    "ragione",
    "ragioni",
    "ragione",
    "ragioni",
    "motivo",
    "motivi",
    "motivo",
    "motivi",
    "piu",
    "più",
    "meno",
    "dire",
    "visto",
    "caso",
    "fatto",
    "volta",
    "volte",
    "tempo",
    "tempi",
    "modo",
    "modi",
    "parte",
    "parti",
    "luogo",
    "luoghi",
    "persona",
    "persone",
    "cosa",
    "cose",
    "ragione",
    "ragioni",
    "motivo",
    "motivi",
    "scopo",
    "scopi",
    "mezzo",
    "mezzi",
    "fine",
    "fini",
    "modo",
    "modi",
    "ragione",
    "ragioni",
    "motivo",
    "motivi",
    "piu",
    "più",
    "meno",
    "meno",
    "tanto",
    "tanto",
    "troppo",
    "troppo",
    "poco",
    "poco",
    "molto",
    "molto",
    "cosi",
    "così",
    "quasi",
    "quasi",
    "abbastanza",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
    "forse",
    "certo",
    "purtroppo",
]


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
    return remove_stopwords(
        lemmatize(basic_clean(text)), extra_words=italianExcludewords
    )


import json
from collections import defaultdict, Counter
import matplotlib.colors as mcolors

with open("sentiment_output_with_offensives.json") as f:
    posts = json.load(f)


source_to_keyword = {
    "paolaegonu_post": "egonu",
    "verovolley_alessiaorro8_post_comments_filtered.json": "orro",
    "verovolley_post_comments_filtered.json": "verovolley",
    "verovolley_miriamsylla_post_comments_filtered.json": "sylla",
    "miriamsylla_post": "sylla",
    "verovolley_crawl": "verovolley",
    "verovolley_paolaegonu_post_comments_filtered.json": "egonu",
}

for post in posts:
    if post["source"] in source_to_keyword:
        keyword = source_to_keyword[post["source"]]
        post["keywords"].append(keyword)

    post["keywords"] = list(set(post["keywords"]))

sentiment_colors = {
    "positive": np.array(mcolors.to_rgb("green")),
    "negative": np.array(mcolors.to_rgb("red")),
    "neutral": np.array(mcolors.to_rgb("gray")),
}

print("cleaning text...", end="\r")
sentiment_text = defaultdict(str)
for post in posts:
    for comment in post["comments"]:
        sentiment = comment["sentiment"]
        if sentiment not in sentiment_colors:
            continue
        if sentiment not in sentiment_text:
            sentiment_text[sentiment] = ""
        sentiment_text[sentiment] += comment["text"] + " "
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
