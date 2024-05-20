import locale
import re
from dateutil import parser
from datetime import datetime

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

def check_format_comment_like(value):
    if isinstance(value, str):
        # Casistica numero con virgola, ad esempio 5,130 = 5130
        if ',' in value: value = value.replace(',', '')
        
        # Casistica numero = Num Likes Not Found / Num Comments Not Found
        # SOLO PER WEB NR LIKES AND COMMENTS = NOT DEFINED (valore fittizio inserito per avere tutto il dict uguale)
        if value in 'Num Likes Not Found' or value in 'Num Comments Not Found' or value in 'Not Defined':
            value = 0
        
        value = int(value)   
    
    return value