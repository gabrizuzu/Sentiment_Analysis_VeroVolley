#!/usr/bin/env python
# coding: utf-8

# In[1]:
import pandas as pd
import matplotlib.pyplot as plt
import json



# In[3]:

def filtered_data(posts):
    filtered_data = []
    for post in posts:

        comments = post['comments']
        filtered_post = {
            'caption_text': post['caption_text'],
            'taken_at_date': post['taken_at'],
            'comment_count': post['comment_count'],
            'like_count': post['like_count'],
            'play_count': post['play_count'],
            'post_author': post['user']['username'],
            'comments' : [{'text': comment['text'], 'username': comment['user']['username'], 'created_at_utc': comment['created_at_utc'],'like_count': comment['like_count']}for comment in comments]
            
        }
        filtered_data.append(filtered_post) 

    return filtered_data




# In[18]:


# questo è il programma che dato in input una parola restituisce i commenti che contengono quella parola
def filter_comments_by_keyword(keyword):
    # Apri il file JSON in lettura
    with open('output.json', 'r') as f:
        data = json.load(f)

    # Filtra i commenti che contengono la parola chiave
    filtered_comments = []
    for post in data:
        comments = post['comments']
        for comment in comments:
            if keyword in comment['text']:
                filtered_comments.append(comment)

    return filtered_comments



# In[19]:

def filter_comments_by_keyword_in_caption(keyword):
    # Apri il file JSON in lettura
    with open('output.json', 'r') as f:
        data = json.load(f)
    # Filtra i post che contengono la parola chiave nel caption_text
    filtered_posts = [post for post in data if keyword in post['caption_text']]

    # Stampa il caption_text e i commenti dei post filtrati
    for post in filtered_posts:
        print("Caption Text:", post['caption_text'])
        print("Comments:")
        for comment in post['comments']:
            print(comment['text'])
        print()


    return filtered_posts


# In[26]:


# In[4]:
# Apri il file JSON in lettura
with open('example.json', 'r') as f:
    data = json.load(f)


# In[2]:


posts = data["media"]
posts

# Scrivi i dati filtrati in un nuovo file JSON con indentazione
with open('output.json', 'w') as f:
    json.dump(filtered_data, f, indent=4)

# Creazione del dataframe con i dati dei post
df = pd.DataFrame(data['media'])
df



# In[27]:


# Seleziona solo le colonne 'like_count' e 'comment_count'
df_counts = df[['like_count', 'comment_count', 'taken_at']]
df_counts




# In[28]:


# Calcola la somma dei likes e dei commenti
total_likes = df_counts['like_count'].sum()
total_comments = df_counts['comment_count'].sum()

total_likes, total_comments

# In[29]:


df_counts.plot(kind='bar')

# In[32]:




# Converti la colonna 'taken_at_date' in formato datetime
df['taken_at'] = pd.to_datetime(df['taken_at'])

# Aggrega i post per mese
df_agg = df.groupby(df['taken_at'].dt.to_period('M')).agg({'like_count': 'sum'})

# Crea il grafico a barre
df_agg.plot(kind='bar')

# Imposta le etichette degli assi
plt.xlabel('Mese')
plt.ylabel('Numero di like')

# Mostra il grafico
plt.show()



# In[33]:


# Converti la colonna 'taken_at_date' in formato datetime
df['taken_at'] = pd.to_datetime(df['taken_at'])

# Aggrega i post per mese
df_agg = df.groupby(df['taken_at'].dt.to_period('M')).agg({'comment_count': 'sum'})

# Crea il grafico a barre
df_agg.plot(kind='bar')

# Imposta le etichette degli assi
plt.xlabel('Mese')
plt.ylabel('Numero di commenti')

# Mostra il grafico
plt.show()


# In[34]:


df_agg
