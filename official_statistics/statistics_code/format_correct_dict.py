from format_values import format_data
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