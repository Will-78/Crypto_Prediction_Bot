'''
This is the layout for the complete script for this project as of now. This does not necessarily
need to be used, but provides a helpful mental map for how everything should work together.
None of the values for the variables have been plugged in yet.
'''
import praw
import openai
import sqlite3
from binance.client import Client

# Configuration
REDDIT_CLIENT_ID = 'YOUR_REDDIT_CLIENT_ID'
REDDIT_CLIENT_SECRET = 'YOUR_REDDIT_CLIENT_SECRET'
REDDIT_USER_AGENT = 'YOUR_REDDIT_USER_AGENT'
OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'
BINANCE_API_KEY = 'YOUR_BINANCE_API_KEY'
BINANCE_API_SECRET = 'YOUR_BINANCE_API_SECRET'
SUBREDDIT = 'cryptocurrency'
LIMIT = 100

# Initialize APIs
reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                     client_secret=REDDIT_CLIENT_SECRET,
                     user_agent=REDDIT_USER_AGENT)

openai.api_key = OPENAI_API_KEY

client = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_API_SECRET)

# Database functions
def create_db():
    conn = sqlite3.connect('crypto_trading.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                 (id TEXT PRIMARY KEY, title TEXT, sentiment TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS trades
                 (id INTEGER PRIMARY KEY, symbol TEXT, side TEXT, quantity REAL)''')
    conn.commit()
    conn.close()

def insert_post(post_id, title, sentiment):
    conn = sqlite3.connect('crypto_trading.db')
    c = conn.cursor()
    c.execute("INSERT INTO posts (id, title, sentiment) VALUES (?, ?, ?)",
              (post_id, title, sentiment))
    conn.commit()
    conn.close()

# Fetch Reddit posts
def fetch_reddit_posts(subreddit, limit=100):
    subreddit = reddit.subreddit(subreddit)
    posts = subreddit.new(limit=limit)
    return posts

# Analyze sentiment
def get_sentiment(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Analyze the sentiment of the following text: {text}",
        max_tokens=60
    )
    sentiment = response.choices[0].text.strip()
    return sentiment

# Get current price of a symbol
def get_current_price(symbol):
    prices = client.get_all_tickers()
    for price in prices:
        if price['symbol'] == symbol:
            return float(price['price'])
    return None

# Determine buy or sell decision based on sentiment
def make_decision(sentiment):
    if 'positive' in sentiment.lower():
        return 'BUY'
    elif 'negative' in sentiment.lower():
        return 'SELL'
    else:
        return 'HOLD'

# Main function
def main():
    create_db()
    posts = fetch_reddit_posts(SUBREDDIT, LIMIT)
    tickers = set()
    
    for post in posts:
        sentiment = get_sentiment(post.title)
        insert_post(post.id, post.title, sentiment)
        
        # Extract ticker symbols (e.g., BTC, ETH) from the post title
        words = post.title.split()
        for word in words:
            if word.isupper() and len(word) <= 5:  # crude check for ticker symbols
                tickers.add(word)
    
    results = []
    for ticker in tickers:
        current_price = get_current_price(ticker + 'USDT')  # assuming USDT pair for simplicity
        if current_price:
            sentiment = get_sentiment(ticker)
            decision = make_decision(sentiment)
            results.append((ticker, current_price, decision))
    
    for result in results:
        print(f"Ticker: {result[0]}, Current Price: {result[1]}, Decision: {result[2]}")

if __name__ == '__main__':
    main()
