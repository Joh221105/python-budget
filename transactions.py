from database import create_connection
import csv


# retrieves all added transactions from transactions table
def get_transactions(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions")
    return cur.fetchall()

# adds transaction as a tuple to transactions table in database

def add_transaction(conn, transaction):
    sql = '''INSERT INTO transactions(type, category, amount, date, notes)
              VALUES(?, ?, ?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, transaction)
    conn.commit()
    return cur.lastrowid

def filter_transactions_by_type(conn, transaction_type):
    cur = conn.cursor()
    sql = '''SELECT * FROM transactions WHERE type = ?'''
    cur.execute(sql, (transaction_type,))
    return cur.fetchall()

def filter_transactions_by_date_range(conn, start_date, end_date):
    cur = conn.cursor()
    sql = '''SELECT * FROM transactions WHERE date BETWEEN ? AND ?'''
    cur.execute(sql, (start_date, end_date))
    return cur.fetchall()

def delete_transaction_by_id(conn, transaction_id):
    sql = '''DELETE FROM transactions WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (transaction_id,))
    conn.commit()
    if cur.rowcount == 0:
        return False  # no transaction found with provided id
    return True 

def update_transaction(conn, transaction_id, updated_transaction):
    sql = '''UPDATE transactions
             SET type = ?, category = ?, amount = ?, date = ?, notes = ?
             WHERE id = ?'''
    
    cur = conn.cursor()
    cur.execute(sql, (*updated_transaction, transaction_id))
    conn.commit()

    if cur.rowcount == 0:
        return False  
    return True  

def get_transaction_by_id(conn, transaction_id):
    sql = '''SELECT * FROM transactions WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (transaction_id,))
    transaction = cur.fetchone()  # fetch one result

    return transaction    # Will return None if the ID doesn't exist

def export_to_csv(conn, filename):
    transactions = get_transactions(conn)    # retrieves all transactions

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
    
        writer.writerow(['ID', 'Type', 'Category', 'Amount', 'Date'])    # write the header
        
        for transaction in transactions:    # write the transaction data
            writer.writerow(transaction)

    print(f"Transactions exported to {filename} successfully.")


def summarize_transactions(conn, start_date, end_date):
    cur = conn.cursor()
    
    # calculates total income
    cur.execute("SELECT SUM(amount) FROM transactions WHERE type = 'income' AND date BETWEEN ? AND ?", (start_date, end_date))
    total_income = cur.fetchone()[0] or 0  # default to 0 if no income
    
    # calculates total expenses
    cur.execute("SELECT SUM(amount) FROM transactions WHERE type = 'expense' AND date BETWEEN ? AND ?", (start_date, end_date))
    total_expenses = cur.fetchone()[0] or 0

    net_balance= total_income - total_expenses

    return total_income, total_expenses, net_balance

def search_transactions_by_notes(conn, keyword):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions WHERE notes LIKE ?", ('%' + keyword + '%',))
    return cursor.fetchall()