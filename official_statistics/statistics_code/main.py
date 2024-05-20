import json
from plot_graph import plot_bar_chart_3data, plot_bar_chart_2data, plot_season
from format_correct_dict import process_post
from utils import count_total_general, count_total_months
from statistics import general_sentiment_posts, months_sentiment_posts, count_sentiment_posts, count_sentiment_comments, count_sentiment_posts_specific, count_sentiment_comments_specific, count_like_posts, count_like_comments, count_like_posts_specific, count_like_comments_specific

# -------------------- LOAD FILE --------------------
def load_data(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
    return data                

# -------------------- MAIN GENERALE --------------------

def main():
    file_path = '/Users/clapcibus/Downloads/sentiment_total.json'
    data = load_data(file_path)
    
    platforms = ['IG', 'FB', 'Web']
    # dict formattato 
    processed_posts = [process_post(post) for post in data]
    
    season_posts_general = general_sentiment_posts(processed_posts)
    total_general = count_total_general(season_posts_general)
    tot_pos_season = [(season_posts_general[1]['positive']/total_general)*100, (season_posts_general[2]['positive']/total_general)*100, (season_posts_general[3]['positive']/total_general)*100]
    tot_neg_season = [(season_posts_general[1]['negative']/total_general)*100, (season_posts_general[2]['negative']/total_general)*100, (season_posts_general[3]['negative']/total_general)*100]
    tot_neu_season = [(season_posts_general[1]['neutral']/total_general)*100, (season_posts_general[2]['neutral']/total_general)*100, (season_posts_general[3]['neutral']/total_general)*100]
    print('Positive ', tot_pos_season)
    print('Negative ', tot_neg_season)
    print('Neutral ', tot_neu_season)
    #plot_season('Seasons', 'Num of posts', 'Sentiment Analysis during each seasons', data1, data2, data3, 'positive', 'negative', 'neutral')
    
    season_posts_months = months_sentiment_posts(processed_posts)
    total_1 = count_total_months(season_posts_months[1])

    for season, count_data in season_posts_months.items(): 
        tot_season_m = [(count_data['positive']/total_1)*100, (count_data['negative']/total_1)*100, (count_data['neutral']/total_1)*100]
        print(f'{season}', tot_season_m)
    
    '''
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
    
    # ---- CONVERT VALUE OF COUNTS IN PERCENTAGE ----
    counts_post = transform_value_in_percentage(counts_post)

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
    '''
    
if __name__ == "__main__":
    main()

