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
                 symbol TEXT,
                 name TEXT
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

def insert_currency(symbol, name):
    conn = sqlite3.connect('crypto_trading.db')
    c = conn.cursor()
    c.execute("INSERT INTO currencies(symbol, name) VALUES(?, ?)",
              (symbol, name))
    c.commit()
    c.close()


