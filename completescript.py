'''
This is the layout for the complete script for this project as of now. This does not necessarily
need to be used, but provides a helpful mental map for how everything should work together.
None of the values for the variables have been plugged in yet.
'''
import asyncio
from binance_api import get_info
from database import *
from gptapi import get_sentiment, make_decision
from redditapi import fetch_reddit_posts

# Configuration
SUBREDDIT = 'cryptocurrency'
LIMIT = 100

# Main function
async def main():
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
    
    for ticker in tickers:

        crypto_id = fetch_currency(ticker)
        if not crypto_id:
            insert_currency(ticker)
            crypto_id = fetch_currency(ticker)

        tick_data, sma, rs, rsi, vwap, book_order = await get_info(ticker + 'USDT')  # assuming USDT pair for simplicity

        sentiment = get_sentiment(ticker)
        decision = make_decision(tick_data, sma, rs, rsi, vwap, book_order, sentiment)
        cache_prediction(crypto_id, decision)
    
        print(f"Ticker: {result[0]}, Current Price: {result[1]}, Decision: {result[2]}")

if __name__ == '__main__':
    asyncio.run(main())
