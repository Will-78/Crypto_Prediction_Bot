# Outline for SQL data base
import sqlite3

def create_db():
    conn = sqlite3.connect('crypto_trading.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS posts
                 (id TEXT PRIMARY KEY, title TEXT, sentiment TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS trades
                 (id INTEGER PRIMARY KEY, symbol TEXT, side TEXT, quantity REAL)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS predictions
                (
                    prediction_id AUTOINCREMENT UNIQUE INTEGER PRIMARY KEY,
                    crypto_id UNIQUE INTEGER,
                    time_stamp TEXT DEFAULT GETDATE(),
                     response TEXT
                )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS currencies
                (
                 crypto_id AUTOINCREMENT UNIQUE INTEGER PRIMARY KEY,
                 symbol TEXT
                )''')
    
    conn.commit()
    conn.close()

def insert_post(post_id, title, sentiment):
    conn = sqlite3.connect('crypto_trading.db')
    c = conn.cursor()
    c.execute("INSERT INTO posts (id, title, sentiment) VALUES (?, ?, ?)",
              (post_id, title, sentiment))
    conn.commit()
    conn.close()

def cache_prediction(crypto_id, response):
    conn = sqlite3.connect('crypto_trading.db')
    c = conn.cursor()
    c.excute("INSERT INTO predictions(crypto_id, response) VALUES(?, ?)",
             (crypto_id, response))
    conn.commit()
    conn.close()

def insert_currency(symbol):
    conn = sqlite3.connect('crypto_trading.db')
    c = conn.cursor()
    c.execute("INSERT INTO currencies(symbol) VALUES(?)",
              (symbol))
    c.commit()
    c.close()

def fetch_currency(symbol):
    conn = sqlite3.connect('crypto-trading.db')
    c = conn.cursor()
    c.execute("SELECT crypto_id FROM currencies WHERE symbol = ?", (symbol))

    crypto_id = c.fetchOne()

    c.close()
    return crypto_id

