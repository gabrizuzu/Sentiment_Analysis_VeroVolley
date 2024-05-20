from format_values import check_format_comment_like

'''
    I dati vogliamo che siano divisi per Seasons.
    Le Seasons sono così definite:
        1. Season 1: from September 2021 to August 2022
        2. Season 2: from September 2022 to August 2023
        3. Season 3: from September 2023 to April 2024
'''

# -------------------- SENTIMENT STATISTICS --------------------

def general_sentiment_posts(posts):
    seasons = {
        1: {'positive': 0, 'negative': 0, 'neutral': 0},
        2: {'positive': 0, 'negative': 0, 'neutral': 0},
        3: {'positive': 0, 'negative': 0, 'neutral': 0}
    }
    
    for post in posts: 
        anno = post['anno']
        mese = post['mese']
        sentiment = post['sentiment_post']
        
        # SEASON 21-22
        if anno == 2021 and 9 <= mese <= 12:
            if sentiment == 'positive': seasons[1]['positive'] += 1
            elif sentiment == 'negative': seasons[1]['negative'] += 1
            elif sentiment == 'neutral': seasons[1]['neutral'] += 1
        
        elif anno == 2022 and 1 <= mese <= 8:
            if sentiment == 'positive': seasons[1]['positive'] += 1
            elif sentiment == 'negative': seasons[1]['negative'] += 1
            elif sentiment == 'neutral': seasons[1]['neutral'] += 1
        
        # SEASON 22-23
        elif anno == 2022 and 9 <= mese <= 12:
            if sentiment == 'positive': seasons[2]['positive'] += 1
            elif sentiment == 'negative': seasons[2]['negative'] += 1
            elif sentiment == 'neutral': seasons[2]['neutral'] += 1
        
        elif anno == 2023 and 1 <= mese <= 8:
            if sentiment == 'positive': seasons[2]['positive'] += 1
            elif sentiment == 'negative': seasons[2]['negative'] += 1
            elif sentiment == 'neutral': seasons[2]['neutral'] += 1
        
        # SEASON 23-24
        elif anno == 2023 and 9 <= mese <= 12:
            if sentiment == 'positive': seasons[3]['positive'] += 1
            elif sentiment == 'negative': seasons[3]['negative'] += 1
            elif sentiment == 'neutral': seasons[3]['neutral'] += 1
        
        elif anno == 2024 and 1 <= mese <= 4:
            if sentiment == 'positive': seasons[3]['positive'] += 1
            elif sentiment == 'negative': seasons[3]['negative'] += 1
            elif sentiment == 'neutral': seasons[3]['neutral'] += 1
    
    return seasons

def months_sentiment_posts(posts):
    seasons = {
        1: {'positive': [0] * 12, 'negative': [0] * 12, 'neutral': [0] * 12},
        2: {'positive': [0] * 12, 'negative': [0] * 12, 'neutral': [0] * 12},
        3: {'positive': [0] * 12, 'negative': [0] * 12, 'neutral': [0] * 12}
    }
    
    for post in posts: 
        anno = post['anno']
        mese = post['mese']
        sentiment = post['sentiment_post']
        
        # SEASON 21-22
        if anno == 2021 and 9 <= mese <= 12:
            if sentiment == 'positive': seasons[1]['positive'][mese - 1] += 1
            elif sentiment == 'negative': seasons[1]['negative'][mese - 1] += 1
            elif sentiment == 'neutral': seasons[1]['neutral'][mese - 1] += 1
        
        elif anno == 2022 and 1 <= mese <= 8:
            if sentiment == 'positive': seasons[1]['positive'][mese - 1] += 1
            elif sentiment == 'negative': seasons[1]['negative'][mese - 1] += 1
            elif sentiment == 'neutral': seasons[1]['neutral'][mese - 1] += 1
        
        # SEASON 22-23
        elif anno == 2022 and 9 <= mese <= 12:
            if sentiment == 'positive': seasons[2]['positive'][mese - 1] += 1
            elif sentiment == 'negative': seasons[2]['negative'][mese - 1] += 1
            elif sentiment == 'neutral': seasons[2]['neutral'][mese - 1] += 1
        
        elif anno == 2023 and 1 <= mese <= 8:
            if sentiment == 'positive': seasons[2]['positive'][mese - 1] += 1
            elif sentiment == 'negative': seasons[2]['negative'][mese - 1] += 1
            elif sentiment == 'neutral': seasons[2]['neutral'][mese - 1] += 1
        
        # SEASON 23-24
        elif anno == 2023 and 9 <= mese <= 12:
            if sentiment == 'positive': seasons[3]['positive'][mese - 1] += 1
            elif sentiment == 'negative': seasons[3]['negative'][mese - 1] += 1
            elif sentiment == 'neutral': seasons[3]['neutral'][mese - 1] += 1
        
        elif anno == 2024 and 1 <= mese <= 4:
            if sentiment == 'positive': seasons[3]['positive'][mese - 1] += 1
            elif sentiment == 'negative': seasons[3]['negative'][mese - 1] += 1
            elif sentiment == 'neutral': seasons[3]['neutral'][mese - 1] += 1
    
    return seasons

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
        nr_like = check_format_comment_like(post['nr_like'])
        nr_comments = check_format_comment_like(post['nr_comment'])
        
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
                    nr_like = check_format_comment_like(post['nr_like'])

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
            nr_like = check_format_comment_like(post['nr_like'])
            nr_comments = check_format_comment_like(post['nr_comment'])

            if anno in count:
                count[anno]['num_likes'][mese - 1] += nr_like
                count[anno]['num_posts'][mese - 1] += 1
                count[anno]['num_comments'][mese - 1] += nr_comments

    return count

# - Comments   
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
                        nr_like = check_format_comment_like(post['nr_like'])

                        if anno in count:
                            count[anno]['num_likes'][mese - 1] += nr_like
                            count[anno]['num_comments'][mese - 1] += 1

    return count

def count_sentiment_posts_season(posts):
    count = {
        'Season 1': {'positive': [0] * 12, 'negative': [0] * 12, 'neutral': [0] * 12},
        'Season 2': {'positive': [0] * 12, 'negative': [0] * 12, 'neutral': [0] * 12},
        'Season 3': {'positive': [0] * 8, 'negative': [0] * 8, 'neutral': [0] * 8}
    }

    for post in posts:
        anno = post['anno']
        mese = post['mese']
        sentiment = post['sentiment_post']

        if anno == 2021 or (anno == 2022 and mese <= 8):
            season = 'Season 1'
        elif anno == 2022 or (anno == 2023 and mese <= 8):
            season = 'Season 2'
        else:
            season = 'Season 3'

        if sentiment == 'positive':
            count[season]['positive'][mese - 1 if season != 'Season 3' else mese - 9] += 1
        elif sentiment == 'negative':
            count[season]['negative'][mese - 1 if season != 'Season 3' else mese - 9] += 1
        elif sentiment == 'neutral':
            count[season]['neutral'][mese - 1 if season != 'Season 3' else mese - 9] += 1

    return count