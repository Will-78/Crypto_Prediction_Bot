# Outline for SQL data base
import sqlite3

async def create_db():
    conn = sqlite3.connect('crypto_trading.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                 (id TEXT PRIMARY KEY, title TEXT, sentiment TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS trades
                 (id INTEGER PRIMARY KEY, symbol TEXT, side TEXT, quantity REAL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS predictions
                (
                    prediction_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                    crypto_id INTEGER,
                    time_stamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    response TEXT
                )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS currencies
                (
                 crypto_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                 symbol TEXT
                )''')
    
    conn.commit()
    conn.close()

async def insert_post(post_id, title, sentiment):
    conn = sqlite3.connect('crypto_trading.db')
    c = conn.cursor()
    c.execute("INSERT INTO posts (id, title, sentiment) VALUES (?, ?, ?)",
              (post_id, title, sentiment))
    conn.commit()
    conn.close()

async def cache_prediction(crypto_id, response):
    conn = sqlite3.connect('crypto_trading.db')
    c = conn.cursor()

    c.execute("INSERT INTO predictions(crypto_id, response) VALUES(?, ?)",
             (crypto_id, response))
    conn.commit()
    conn.close()

async def insert_currency(symbol):
    conn = sqlite3.connect('crypto_trading.db')
    c = conn.cursor()
    c.execute("INSERT INTO currencies(symbol) VALUES(?)",
              (symbol,))
    conn.commit()
    conn.close()

async def fetch_currency(symbol):
    conn = sqlite3.connect('crypto_trading.db')
    c = conn.cursor()
    c.execute("SELECT crypto_id FROM currencies WHERE symbol = ?", (symbol,))

    crypto_id = c.fetchone() # it returns a tuple

    if crypto_id:
        crypto_id=crypto_id[0] 

    conn.close()
    return crypto_id

async def fetch_prediction(crypto_id):
    conn = sqlite3.connect('crypto_trading.db')
    c = conn.cursor()
    c.execute('''SELECT time_stamp, response
                 FROM predictions
                 WHERE crypto_id = ? ''',
                 (crypto_id,))
    data = c.fetchall()
    timestamps, responses = [], []

    if data:

        for analysis in data:
            timestamps.append(analysis[0])
            responses.append(analysis[1])

    conn.close()
    return timestamps, responses
