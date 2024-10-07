from database import create_connection


# retrieves all added transactions from transactions table
def get_transactions(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions")
    return cur.fetchall()