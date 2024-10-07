from database import create_connection


# retrieves all added transactions from transactions table
def get_transactions(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions")
    return cur.fetchall()

# adds transaction as a tuple to transactions table in database

def add_transaction(conn, transaction):
    sql = '''INSERT INTO transactions(type, category, amount, date)
              VALUES(?, ?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, transaction)
    conn.commit()
    return cur.lastrowid
