import sqlite3

def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn

