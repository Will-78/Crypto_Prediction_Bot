# Outline for SQL data base
import sqlite3

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
