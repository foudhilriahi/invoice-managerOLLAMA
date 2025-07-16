import sqlite3
from config import DATABASE_FILE
import json

def init_db():
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            raw_json TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_invoice(data):
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    json_str = json.dumps(data, ensure_ascii=False)
    cur.execute('INSERT INTO invoices (raw_json) VALUES (?)', (json_str,))
    conn.commit()
    conn.close()

def fetch_all_invoices():
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute('SELECT id, raw_json FROM invoices ORDER BY id DESC')
    rows = cur.fetchall()
    conn.close()
    return rows

def fetch_invoice_raw_json(invoice_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cur = conn.cursor()
    cur.execute('SELECT raw_json FROM invoices WHERE id=?', (invoice_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None
