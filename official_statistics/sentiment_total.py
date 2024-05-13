import json
import locale
import re
from dateutil import parser
from datetime import datetime

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

def check_year_present(date_str):
    # Espressione regolare per cercare un anno nel formato 'YYYY'
    year_pattern = r"\b\d{4}\b"

    # Cerca un anno nella stringa data
    match = re.search(year_pattern, date_str)

    # Restituisci True se l'anno è presente, False altrimenti
    return match is not None

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

    # CASO 3: formato data accettabile (IN TEORIA !!!)
    else:
        try:
            # prova a formattare se realmente la data è in un formato accettabile
            return parser.parse(data)
        except ValueError:
            # Se fallisce, prova con il mese scritto nel formato abbrevviato
            # Esempio:
            # 5 giu 2023
            return datetime.strptime(data, '%d %b %Y')
    
#OPEN FILE
with open('/Users/clapcibus/Downloads/sentiment_total.json', 'r') as f:
    data = json.load(f)
    
arrayTot = []

for post in data:
    platform = post.get('platform')
    
    #INSTAGRAM 
    if platform == 'IG':
        data_pubblicazione = format_data(post['taken_at_date'])
        
        postSing = {
            'platform' : platform,
            'source': post['source'],
            'giorno': data_pubblicazione.day,
            'mese': data_pubblicazione.month,
            'anno': data_pubblicazione.year,
            'sentiment_post': post['sentiment'],
            'nr_like': post['likes_count'],
            'nr_comment' : post['comments_count'],
            'comments': []
        }
        
        comments = post.get('comments', [])
        for comment in comments:
            data_comm = format_data(comment['created_at_utc'])
            
            comm = {
                'author': comment['username'],
                'giorno': data_comm.day,
                'mese': data_comm.month,
                'anno': data_comm.year,
                'sentiment_comment': comment['sentiment'],
                'nr_like' : comment['like_count']
            }
            
            postSing['comments'].append(comm)
    
        arrayTot.append(postSing)
   
    #FACEBOOK
    elif platform == 'FB':
        data_pubblicazione = format_data(post['date'])

        postSing = {
            'platform' : platform,
            'source': post['source'],
            'giorno': data_pubblicazione.day,
            'mese': data_pubblicazione.month,
            'anno': data_pubblicazione.year,
            'sentiment_post': post['sentiment'],
            'nr_like': post['num_likes'],
            'nr_comment' : post['num_comments'],
            'comments': []
        }
        
        comments = post.get('comments', [])
        for comment in comments:
            data_comm = format_data(comment['date'])
            
            comm = {
                'author': comment['author'],
                'giorno': data_comm.day,
                'mese': data_comm.month,
                'anno': data_comm.year,
                'sentiment_comment': comment['sentiment'],
                'nr_like' : comment['likes_num']
            }
            
            postSing['comments'].append(comm)
    
        arrayTot.append(postSing)
    
    #WEB
    elif platform == 'Web':
        data_pubblicazione = format_data(post['date'])
        
        postSing = {
            'platform' : platform,
            'source': post['source'],
            'giorno': data_pubblicazione.day,
            'mese': data_pubblicazione.month,
            'anno': data_pubblicazione.year,
            'sentiment_post': post['sentiment'],
            'comments': []
        }
        
        '''
        #!!!! da completare tutti i post del web per ora non hanno commenti !!!!
        comments = post.get('comments', [])
        
        for comment in comments:
            data_comm = parse_data(comment['created_at_utc'])
            
            comm = {
                'author': comment['author'],
                'giorno': data_comm.day,
                'mese': data_comm.month,
                'anno': data_comm.year,
                'sentiment_comment': comment['sentiment'],
                'nr_like' : comment['likes_num']
            }
            
            postSing['comments'].append(comm)
        '''
        postSing['comments'].append(comments)
        arrayTot.append(postSing)    

# ora arrayTot contiene tutti i dati scritti nel formato: 
#               - platform
#               - source
#               - giorno
#               - mese
#               - anno 
#               - sentiment_post
#           !!! SOLO PER IG & FB !!!
#               - nr_like
#               - nr_comments
#               - comments {
#                   - author
#                   - giorno
#                   - mese
#                   - anno
#                   - sentiment_comment
#                   - nr_like    


# ----- POST -----
count_pos = [0] * 12
count_neg = [0] * 12
count_neu = [0] * 12
count_pos_2 = [0] * 12
count_neg_2 = [0] * 12
count_neu_2 = [0] * 12
count_pos_3 = [0] * 12
count_neg_3 = [0] * 12
count_neu_3 = [0] * 12
count_pos_4 = [0] * 12
count_neg_4 = [0] * 12
count_neu_4 = [0] * 12

count_pos_v = [0] * 12
count_neg_v = [0] * 12
count_neu_v = [0] * 12
count_pos_2_v = [0] * 12
count_neg_2_v = [0] * 12
count_neu_2_v = [0] * 12
count_pos_3_v = [0] * 12
count_neg_3_v = [0] * 12
count_neu_3_v = [0] * 12
count_pos_4_v = [0] * 12
count_neg_4_v = [0] * 12
count_neu_4_v = [0] * 12

count_post = 0

# STATISTICHE GENERALI
for post in arrayTot:
    anno = post['anno']
    mese = post['mese']
    sentiment = post['sentiment_post']
    
    #STATICHE POST SOLO DI VEROVOLLEY
    if 'verovolley' in post['source']:
        if anno == 2024:
            count_list = count_pos_v if sentiment == 'positive' else (count_neg_v if sentiment == 'negative' else count_neu_v)
            count_list[mese - 1] += 1

        elif anno == 2023:
            count_list = count_pos_2_v if sentiment == 'positive' else (count_neg_2_v if sentiment == 'negative' else count_neu_2_v)
            count_list[mese - 1] += 1
        
        elif anno == 2022:
            count_list = count_pos_3_v if sentiment == 'positive' else (count_neg_3_v if sentiment == 'negative' else count_neu_3_v)
            count_list[mese - 1] += 1
        
        elif anno == 2021:
            count_list = count_pos_4_v if sentiment == 'positive' else (count_neg_4_v if sentiment == 'negative' else count_neu_4_v)
            count_list[mese - 1] += 1
        
        count_post+=1
   
    #STATISTICHE POST SENZA VEROVOLLEY
    else:
        if anno == 2024:
            count_list = count_pos if sentiment == 'positive' else (count_neg if sentiment == 'negative' else count_neu)
            count_list[mese - 1] += 1

        elif anno == 2023:
            count_list = count_pos_2 if sentiment == 'positive' else (count_neg_2 if sentiment == 'negative' else count_neu_2)
            count_list[mese - 1] += 1
        
        elif anno == 2022:
            count_list = count_pos_3 if sentiment == 'positive' else (count_neg_3 if sentiment == 'negative' else count_neu_3)
            count_list[mese - 1] += 1
        
        elif anno == 2021:
            count_list = count_pos_4 if sentiment == 'positive' else (count_neg_4 if sentiment == 'negative' else count_neu_4)
            count_list[mese - 1] += 1

    count_post += 1
        
print("NUMBER OF POST ", count_post)
print("")
print("2024")
print("Positive ", count_pos)
print("Negative ", count_neg)
print("Neutral ", count_neu)
print("")
print("2023")
print("Positive ", count_pos_2)
print("Negative ", count_neg_2)
print("Neutral ", count_neu_2)
print("")
print("2022")
print("Positive ", count_pos_3)
print("Negative ", count_neg_3)
print("Neutral ", count_neu_3)
print("")
print("2021")
print("Positive ", count_pos_4)
print("Negative ", count_neg_4)
print("Neutral ", count_neu_4)
print("")
print("VEROVOLLEY")
print("2024")
print("Positive ", count_pos_v)
print("Negative ", count_neg_v)
print("Neutral ", count_neu_v)
print("")
print("2023")
print("Positive ", count_pos_2_v)
print("Negative ", count_neg_2_v)
print("Neutral ", count_neu_2_v)
print("")
print("2022")
print("Positive ", count_pos_3_v)
print("Negative ", count_neg_3_v)
print("Neutral ", count_neu_3_v)
print("")
print("2021")
print("Positive ", count_pos_4_v)
print("Negative ", count_neg_4_v)
print("Neutral ", count_neu_4_v)


'''
# ----- COMMENTS -----
for post in data:
    anno = post['anno']
    mese = post['mese']
    sentiment = post['sentiment']

    if anno == 2024:
        count_list = count_pos if sentiment == 'positive' else (count_neg if sentiment == 'negative' else count_neu)
        count_list[mese - 1] += 1

    elif anno == 2023:
        count_list = count_pos_2 if sentiment == 'positive' else (count_neg_2 if sentiment == 'negative' else count_neu_2)
        count_list[mese - 1] += 1
    
    elif anno == 2022:
        count_list = count_pos_3 if sentiment == 'positive' else (count_neg_3 if sentiment == 'negative' else count_neu_3)
        count_list[mese - 1] += 1
    
    elif anno == 2021:
        count_list = count_pos_4 if sentiment == 'positive' else (count_neg_4 if sentiment == 'negative' else count_neu_4)
        count_list[mese - 1] += 1

    count_post += 1
'''
