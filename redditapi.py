import praw

reddit = praw.Reddit(client_id='YOUR_CLIENT_ID',
                     client_secret='YOUR_CLIENT_SECRET',
                     user_agent='YOUR_USER_AGENT')

def fetch_reddit_posts(subreddit, limit=100):
    subreddit = reddit.subreddit(subreddit)
    posts = subreddit.new(limit=limit)
    return posts
