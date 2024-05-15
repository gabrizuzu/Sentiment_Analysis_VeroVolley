import json
import locale
import re
from dateutil import parser
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

# -------------------- LOAD FILE --------------------
def load_data(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data


# -------------------- FORMAT DATA --------------------

# - Se anno presente nella stringa
def check_year_present(date_str):
    # Espressione regolare per cercare un anno nel formato 'YYYY'
    year_pattern = r"\b\d{4}\b"

    # Cerca un anno nella stringa data
    match = re.search(year_pattern, date_str)

    # Restituisci True se l'anno è presente, False altrimenti
    return match is not None


# - Se anno contiene un giorno della settimana 
def contains_weekday(string):
    week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
                 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'
                 'Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica',
                 'lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato', 'domenica'
                ]
    for day in week_days:
        if day in string:
            return True
    return False


# - Aggiunta anno ne non presente
def add_year_to_date(data):
    # 1) VERIFICA SE NELLA STRINGA È PRESENTE L'ANNO => 
    # se ok allora procede con la formattazione
    if check_year_present(data):
        try:
            # Prova a convertire la data con il mese scritto per intero 
            data = datetime.strptime(data, "%d %B %Y %H:%M")
        except ValueError:
            # Se fallisce, prova con il mese scritto nel formato abbrevviato
            data = datetime.strptime(data, '%d %b %Y %H:%M')
        
        return data
    
    # 2) ANNO NELLA STRINGA NON PRESENTE =>
    # se non presente allora si fa riferimento all'anno corrente
    else:
        # estraggo anno corrente
        current_year = datetime.now().year
        # aggiungo anno alla stringa 
        data = f"{data} {current_year}"
        
        try:
            # Prova a convertire la data con il mese scritto per intero
            data = datetime.strptime(data, "%d %B %H:%M %Y")
        except ValueError:
            # Se fallisce, prova con il mese scritto nel formato abbrevviato
            data = datetime.strptime(data, '%d %b %H:%M %Y')
            
        return data
    
# - Format data
def format_data(data):
    # CASO 1
    # "Today at 12:04" 
    # "Yesterday at 10:46"
    # "Ieri alle 06:29"
    # "sabato alle 23:08"
    # "19 hrs"
    # "Date Not Found"
    # "45 minutes ago"
    # !!! Tali date verranno convertite nel formato 2024-05-01 00:00:00
    if "Yesterday" in data or "Today" in data or "hrs" in data or contains_weekday(data) or "Date Not Found" in data or "ago" in data or "Ieri" in data: 
        data = "2024-05"
        return datetime.strptime(data, "%Y-%m")
    
    # CASO 2
    # data contenente "alle" o "alle ore"
    # Esempio: 
    # "3 maggio alle ore 01:00"
    elif "ore" in data or "alle" in data:
        locale.setlocale(locale.LC_TIME, "it_IT.UTF-8")
        data = data.replace(" alle ore ", " ").replace(" alle ", " ")
        return add_year_to_date(data)

    # CASO 3: 
    else:
        try:
            # data formato "10/6/2022, 15:33"
            return datetime.strptime(data, "%d/%m/%Y, %H:%M")
        except ValueError:
            try:
                # data formato "24/1/2024"
                return datetime.strptime(data, "%d/%m/%Y")
            except ValueError:
                try: 
                    # data formato "5 giu 2023"
                    return datetime.strptime(data, '%d %b %Y')
                except ValueError:
                    # data formato accettabile (SI SPERA.....)
                    return parser.parse(data)

def check_format__comment_like(value):
    if isinstance(value, str):
        # Casistica numero con virgola, ad esempio 5,130 = 5130
        if ',' in value: value = value.replace(',', '')
        
        # Casistica numero = Num Likes Not Found / Num Comments Not Found
        # SOLO PER WEB NR LIKES AND COMMENTS = NOT DEFINED (valore fittizio inserito per avere tutto il dict uguale)
        if value in 'Num Likes Not Found' or value in 'Num Comments Not Found' or value in 'Not Defined':
            value = 0
        
        value = int(value)   
    
    return value                   

# -------------------- SENTIMENT STATISTICS --------------------

# GENERAL
# - Posts
def count_sentiment_posts(posts):
    count = {
        2021: {'positive': [0] * 12, 'negative': [0] * 12, 'neutral': [0] * 12},
        2022: {'positive': [0] * 12, 'negative': [0] * 12, 'neutral': [0] * 12},
        2023: {'positive': [0] * 12, 'negative': [0] * 12, 'neutral': [0] * 12},
        2024: {'positive': [0] * 12, 'negative': [0] * 12, 'neutral': [0] * 12}
    }

    for post in posts:
        anno = post['anno']
        mese = post['mese']
        sentiment = post['sentiment_post']

        if anno in count:
            if sentiment == 'positive': count[anno]['positive'][mese - 1] += 1
            elif sentiment == 'negative': count[anno]['negative'][mese - 1] += 1
            elif sentiment == 'neutral': count[anno]['neutral'][mese - 1] += 1

    return count
    
# - Comments
def count_sentiment_comments(posts):
    count = {
        2021: {'positive': [0] * 12, 'negative': [0] * 12, 'neutral': [0] * 12},
        2022: {'positive': [0] * 12, 'negative': [0] * 12, 'neutral': [0] * 12},
        2023: {'positive': [0] * 12, 'negative': [0] * 12, 'neutral': [0] * 12},
        2024: {'positive': [0] * 12, 'negative': [0] * 12, 'neutral': [0] * 12}
    }

    for post in posts:
        comments = post.get('comments', [])
        
        for comment in comments:
                if "verovolley" not in comment.get('author'):
                    anno = comment.get('anno')
                    mese = comment.get('mese')
                    sentiment = comment.get('sentiment_comment')

                    if anno in count:
                        if sentiment == 'positive': count[anno]['positive'][mese - 1] += 1
                        elif sentiment == 'negative': count[anno]['negative'][mese - 1] += 1
                        elif sentiment == 'neutral': count[anno]['neutral'][mese - 1] += 1

    return count

# SPECIFIC
# - Posts
def count_sentiment_posts_specific(posts, platform):
    count = {
        2021: {'positive': [0] * 12, 'negative': [0] * 12, 'neutral': [0] * 12},
        2022: {'positive': [0] * 12, 'negative': [0] * 12, 'neutral': [0] * 12},
        2023: {'positive': [0] * 12, 'negative': [0] * 12, 'neutral': [0] * 12},
        2024: {'positive': [0] * 12, 'negative': [0] * 12, 'neutral': [0] * 12}
    }

    for post in posts:
        if post['platform'] == platform:
            anno = post['anno']
            mese = post['mese']
            sentiment = post['sentiment_post']

            if anno in count:
                if sentiment == 'positive': count[anno]['positive'][mese - 1] += 1
                elif sentiment == 'negative': count[anno]['negative'][mese - 1] += 1
                elif sentiment == 'neutral' : count[anno]['neutral'][mese - 1] += 1

    return count

# - Comments
def count_sentiment_comments_specific(posts, platform):
    count = {
        2021: {'positive': [0] * 12, 'negative': [0] * 12, 'neutral': [0] * 12},
        2022: {'positive': [0] * 12, 'negative': [0] * 12, 'neutral': [0] * 12},
        2023: {'positive': [0] * 12, 'negative': [0] * 12, 'neutral': [0] * 12},
        2024: {'positive': [0] * 12, 'negative': [0] * 12, 'neutral': [0] * 12}
    }

    for post in posts:
        if post['platform'] == platform:
            comments = post.get('comments', [])
            
            for comment in comments:
                    if "verovolley" not in comment.get('author'):
                        anno = comment.get('anno')
                        mese = comment.get('mese')
                        sentiment = comment.get('sentiment_comment')

                        if anno in count:
                            if sentiment == 'positive': count[anno]['positive'][mese - 1] += 1
                            elif sentiment == 'negative': count[anno]['negative'][mese - 1] += 1
                            elif sentiment == 'neutral': count[anno]['neutral'][mese - 1] += 1

    return count

# -------------------- COUNT LIKES AND COMMENTS FOR THE STATISTICS --------------------

# GENERAL
# - Posts
def count_like_posts(posts):
    count = {
        2021: {'num_likes': [0] * 12, 'num_posts': [0] * 12, 'num_comments': [0] * 12},
        2022: {'num_likes': [0] * 12, 'num_posts': [0] * 12, 'num_comments': [0] * 12},
        2023: {'num_likes': [0] * 12, 'num_posts': [0] * 12, 'num_comments': [0] * 12},
        2024: {'num_likes': [0] * 12, 'num_posts': [0] * 12, 'num_comments': [0] * 12}
    }

    for post in posts:
        anno = post['anno']
        mese = post['mese']
        nr_like = check_format__comment_like(post['nr_like'])
        nr_comments = check_format__comment_like(post['nr_comment'])
        
        if anno in count:
            count[anno]['num_likes'][mese - 1] += nr_like                    
            count[anno]['num_posts'][mese - 1] += 1
            count[anno]['num_comments'][mese - 1] += nr_comments

    return count
    
# - Comments
def count_like_comments(posts):
    count = {
        2021: {'num_likes': [0] * 12, 'num_comments': [0] * 12},
        2022: {'num_likes': [0] * 12, 'num_comments': [0] * 12},
        2023: {'num_likes': [0] * 12, 'num_comments': [0] * 12},
        2024: {'num_likes': [0] * 12, 'num_comments': [0] * 12}
    }

    for post in posts:
        comments = post.get('comments', [])
        
        for comment in comments:
                if "verovolley" not in comment.get('author'):
                    anno = comment.get('anno')
                    mese = comment.get('mese')
                    nr_like = 0
                    nr_like = check_format__comment_like(post['nr_like'])

                    if anno in count:
                        count[anno]['num_likes'][mese - 1] += nr_like                    
                        count[anno]['num_comments'][mese - 1] += 1

    return count

# SPECIFIC
# - Posts
def count_like_posts_specific(posts, platform):
    count = {
        2021: {'num_likes': [0] * 12, 'num_posts': [0] * 12, 'num_comments': [0] * 12},
        2022: {'num_likes': [0] * 12, 'num_posts': [0] * 12, 'num_comments': [0] * 12},
        2023: {'num_likes': [0] * 12, 'num_posts': [0] * 12, 'num_comments': [0] * 12},
        2024: {'num_likes': [0] * 12, 'num_posts': [0] * 12, 'num_comments': [0] * 12}
    }

    for post in posts:
        if post['platform'] == platform:
            anno = post['anno']
            mese = post['mese']
            nr_like = 0
            nr_like = check_format__comment_like(post['nr_like'])
            nr_comments = check_format__comment_like(post['nr_comment'])

            if anno in count:
                count[anno]['num_likes'][mese - 1] += nr_like
                count[anno]['num_posts'][mese - 1] += 1
                count[anno]['num_comments'][mese - 1] += nr_comments

    return count

# - Comments    ??? MA È SENSATA ???
def count_like_comments_specific(posts, platform):
    count = {
        2021: {'num_likes': [0] * 12, 'num_comments': [0] * 12},
        2022: {'num_likes': [0] * 12, 'num_comments': [0] * 12},
        2023: {'num_likes': [0] * 12, 'num_comments': [0] * 12},
        2024: {'num_likes': [0] * 12, 'num_comments': [0] * 12}
    }

    for post in posts:
        if post['platform'] == platform:
            comments = post.get('comments', [])
            
            for comment in comments:
                    if "verovolley" not in comment.get('author'):
                        anno = comment.get('anno')
                        mese = comment.get('mese')
                        nr_like = 0
                        nr_like = check_format__comment_like(post['nr_like'])

                        if anno in count:
                            count[anno]['num_likes'][mese - 1] += nr_like
                            count[anno]['num_comments'][mese - 1] += 1

    return count


# -------------------- PLOT THE STATISTICS --------------------

def plot_bar_chart_3data(xlabel, ylabel, title, data1, data2, data3, label1, label2, label3):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    x = np.arange(len(months))  # the label locations
    width = 0.18 # the width of the bars

    fig, ax = plt.subplots(figsize=(12,8))
    rects1 = ax.bar(x - width, data1, width, color='#20519F', label=f'{label1}')
    rects2 = ax.bar(x, data2, width, color='#e14547', label=f'{label2}')
    rects3 = ax.bar(x + width, data3, width, color='#A8D9FD', label=f'{label3}')
    
    # valori settati in scala logaritmica per una miglior presentazione dei dati
    ax.set_yscale('log')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel(f'{xlabel}', fontweight='bold')
    ax.set_ylabel(f'{ylabel}', fontweight='bold')
    ax.set_title(f'{title}', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(months, rotation=45, ha='right')
    ax.legend()

    ax.bar_label(rects1, padding=5, fontsize=8, fontweight='bold')
    ax.bar_label(rects2, padding=5, fontsize=8, fontweight='bold')
    ax.bar_label(rects3, padding=5, fontsize=8, fontweight='bold')

    fig.tight_layout()
    plt.savefig(f'{title}')
    plt.show()


def plot_bar_chart_2data(xlabel, ylabel, title, data1, data2, label1, label2):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    x = np.arange(len(months))  # the label locations
    width = 0.18  # the width of the bars

    fig, ax = plt.subplots(figsize=(12,8))
    rects1 = ax.bar(x - width/2, data1, width, color='#20519F', label=f'{label1}')
    rects2 = ax.bar(x + width/2, data2, width, color='#e14547', label=f'{label2}')
    
    # valori settati in scala logaritmica per una miglior presentazione dei dati
    ax.set_yscale('log')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel(f'{xlabel}', fontweight='bold')
    ax.set_ylabel(f'{ylabel}', fontweight='bold')
    ax.set_title(f'{title}', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(months, rotation=45, ha='right')
    ax.legend()

    ax.bar_label(rects1, padding=5, fontsize=8, fontweight='bold')
    ax.bar_label(rects2, padding=5, fontsize=8, fontweight='bold')

    fig.tight_layout()
    plt.savefig(f'{title}')
    plt.show()

# OTTENIAMO UN UNICO DICT FORMATTATO NEL SEGUENTE MODO:
#               - platform
#               - source
#               - giorno
#               - mese
#               - anno 
#               - sentiment_post
#               - nr_like
#               - nr_comment
#               - comments {
#                   - author
#                   - giorno
#                   - mese
#                   - anno
#                   - sentiment_comment
#                   - nr_like (X WEB IMPOSTATI A 0)
#                 }
def process_post(post):  
    platform = post['platform']
        
    #INSTAGRAM 
    if platform == 'IG':
        data_pubblicazione_IG = format_data(post['taken_at_date'])
        
        if 'verovolley' in post['source']:
            postSing = {
                'platform' : platform,
                'source': post['source'],
                'giorno': data_pubblicazione_IG.day,
                'mese': data_pubblicazione_IG.month,
                'anno': data_pubblicazione_IG.year,
                'sentiment_post': 'none',
                'nr_like': post['likes_count'],
                'nr_comment' : post['comments_count'],
                'comments': []
            }
        else:
            postSing = {
                'platform' : platform,
                'source': post['source'],
                'giorno': data_pubblicazione_IG.day,
                'mese': data_pubblicazione_IG.month,
                'anno': data_pubblicazione_IG.year,
                'sentiment_post': post['sentiment'],
                'nr_like': post['likes_count'],
                'nr_comment' : post['comments_count'],
                'comments': []
            }
            
        for comment_IG in post.get('comments', []):
            data_comm_IG = format_data(comment_IG['created_at_utc'])
            
            comm_IG = {
                'author': comment_IG['username'],
                'giorno': data_comm_IG.day,
                'mese': data_comm_IG.month,
                'anno': data_comm_IG.year,
                'sentiment_comment': comment_IG['sentiment'],
                'nr_like' : comment_IG['like_count']
            }
            
            postSing['comments'].append(comm_IG) 
              
    #FACEBOOK
    elif platform == 'FB':
        data_pubblicazione_FB = format_data(post['date'])

        if 'verovolley' in post['source']:
            postSing = {
                'platform' : platform,
                'source': post['source'],
                'giorno': data_pubblicazione_FB.day,
                'mese': data_pubblicazione_FB.month,
                'anno': data_pubblicazione_FB.year,
                'sentiment_post': 'none',
                'nr_like': post['num_likes'],
                'nr_comment' : post['num_comments'],
                'comments': []
            }
        
        else:
            postSing = {
                'platform' : platform,
                'source': post['source'],
                'giorno': data_pubblicazione_FB.day,
                'mese': data_pubblicazione_FB.month,
                'anno': data_pubblicazione_FB.year,
                'sentiment_post': post['sentiment'],
                'nr_like': post['num_likes'],
                'nr_comment' : post['num_comments'],
                'comments': []
            }
        
        for comment_FB in post.get('comments', []):
            data_comm_FB = format_data(comment_FB['date'])
            
            comm_FB = {
                'author': comment_FB['author'],
                'giorno': data_comm_FB.day,
                'mese': data_comm_FB.month,
                'anno': data_comm_FB.year,
                'sentiment_comment': comment_FB['sentiment'],
                'nr_like' : comment_FB['likes_num']
            }
            
            postSing['comments'].append(comm_FB)

    #WEB
    elif platform == 'Web':
        data_pubblicazione_Web = format_data(post['date'])
  
        if 'verovolley' in post['source']:   
            postSing = {
                'platform' : platform,
                'source': post['source'],
                'giorno': data_pubblicazione_Web.day,
                'mese': data_pubblicazione_Web.month,
                'anno': data_pubblicazione_Web.year,
                'sentiment_post': 'none',
                'nr_like': 'Not Defined',
                'nr_comment' : 'Not Defined',
                'comments': []
            }
        
        else:
            postSing = {
                'platform' : platform,
                'source': post['source'],
                'giorno': data_pubblicazione_Web.day,
                'mese': data_pubblicazione_Web.month,
                'anno': data_pubblicazione_Web.year,
                'sentiment_post': post['sentiment'],
                'nr_like': 'Not Defined',
                'nr_comment' : 'Not Defined',
                'comments': []
            }
        
        for comment_Web in post.get('comments', []):
            data_comm_Web = format_data(comment_Web['created_at_utc'])
            
            comm_Web = {
                'author': comment_Web['user'],
                'giorno': data_comm_Web.day,
                'mese': data_comm_Web.month,
                'anno': data_comm_Web.year,
                'sentiment_comment': comment_Web['sentiment'],
                'nr_like': '0'
            }
            
            postSing['comments'].append(comm_Web)
    
    return postSing

# -------------------- MAIN GENERALE --------------------

def main():
    file_path = '/Users/clapcibus/Downloads/sentiment_total.json'
    data = load_data(file_path)
    
    platforms = ['IG', 'FB', 'Web']
    # dict formattato 
    processed_posts = [process_post(post) for post in data]
    
    # GENERALI
    # - Posts
    counts_post = count_sentiment_posts(processed_posts)
    
    # - Comments
    counts_comments = count_sentiment_comments(processed_posts)
   
   
    # SPECIFICI PER PIATTAFORMA
    # - Posts
    counts_posts_specific = {}
    for platform in platforms:
        counts_posts_specific[platform] = count_sentiment_posts_specific(processed_posts, platform)
        
    # - Comments 
    counts_comments_specific = {}
    for platform in platforms:
        counts_comments_specific[platform] = count_sentiment_comments_specific(processed_posts, platform)
    
    
    # COUNT NR OF LIKES AND COMMENTS
    
    # GENERALI
    # - Posts
    counts_likes_post = count_like_posts(processed_posts)
    
    # - Comments
    counts_likes_comments = count_like_comments(processed_posts)
   
   
    # SPECIFICI PER PIATTAFORMA
    # - Posts
    counts_like_posts_specific = {}
    for platform in platforms:
        counts_like_posts_specific[platform] = count_like_posts_specific(processed_posts, platform)
        
    # - Comments
    counts_like_comments_specific = {}
    for platform in platforms:
        counts_like_comments_specific[platform] = count_like_comments_specific(processed_posts, platform)
    
    
    # ---- PLOT ----
    
    # Statistiche generali
    # - Post
    for year, count_data in counts_post.items():
        plot_bar_chart_3data('Months', 'Num of posts', f'Sentiment Analysis of Posts - {year}', count_data['positive'], count_data['negative'], count_data['neutral'], 'positive', 'negative', 'neutral')
    
    # - Comments
    for year, count_data in counts_comments.items():
        plot_bar_chart_3data('Months', 'Num of comments', f'Sentiment Analysis of Comments - {year}', count_data['positive'], count_data['negative'], count_data['neutral'], 'positive', 'negative', 'neutral')
        
    # Statistiche specifiche per piattaforma
    # - Post
    for platform, counts in counts_posts_specific.items():
        for year, count_data in counts.items():
            plot_bar_chart_3data('Months', 'Num of posts', f'{platform} Sentiment Analysis of Posts - {year}', count_data['positive'], count_data['negative'], count_data['neutral'], 'positive', 'negative', 'neutral')
    
    # - Comments
    for platform, counts in counts_comments_specific.items():
        for year, count_data in counts.items():
            plot_bar_chart_3data('Months', 'Num of comments', f'{platform} Sentiment Analysis of Comments - {year}', count_data['positive'], count_data['negative'], count_data['neutral'], 'positive', 'negative', 'neutral')
    
     
    # COUNT NR OF LIKES AND COMMENTS
    
    # Generali
    # - Post
    for year, count_data in counts_likes_post.items():
        plot_bar_chart_3data('Months', 'Values', f'Comprehensive Analysis of Posts Statistics - {year}', count_data['num_likes'], count_data['num_posts'], count_data['num_comments'], 'likes of posts', 'posts', 'comments')
    
    # - Comments
    for year, count_data in counts_likes_comments.items():
        plot_bar_chart_2data('Months', 'Values', f'Comprehensive Analysis of Comments Statistics - {year}', count_data['num_likes'], count_data['num_comments'], 'likes of comments', 'comments')
    
        
    # Specifiche per piattaforma
    # - Post
    for platform, counts in counts_like_posts_specific.items():
        for year, count_data in counts.items():
            plot_bar_chart_3data('Months', 'Values', f'{platform} Posts Analysis - {year}', count_data['num_likes'], count_data['num_posts'], count_data['num_comments'], 'likes of posts', 'posts', 'comments')
        
    # - Comments
    for platform, counts in counts_like_comments_specific.items():
        for year, count_data in counts.items():
            plot_bar_chart_2data('Months', 'Values', f'{platform} Comments Analysis - {year}', count_data['num_likes'], count_data['num_comments'], 'likes of comments', 'comments')
     
    
if __name__ == "__main__":
    main()

