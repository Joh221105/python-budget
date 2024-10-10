import sqlite3

def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn

def create_table(conn):
    try:
        sql = '''CREATE TABLE IF NOT EXISTS transactions (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     type TEXT NOT NULL,
                     category TEXT NOT NULL,
                     amount REAL NOT NULL,
                     date TEXT NOT NULL
                 );'''
        conn.execute(sql)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

    