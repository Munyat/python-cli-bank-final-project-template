import sqlite3

def get_connection():
    return sqlite3.connect('bank.db')

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS account_holder (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS account (
                        id INTEGER PRIMARY KEY,
                        account_number TEXT NOT NULL,
                        balance REAL NOT NULL,
                        account_holder_id INTEGER,
                        account_type TEXT,
                        FOREIGN KEY (account_holder_id) REFERENCES account_holder(id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS "transaction" (
                        id INTEGER PRIMARY KEY,
                        account_id INTEGER,
                        amount REAL,
                        type TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (account_id) REFERENCES account(id))''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
