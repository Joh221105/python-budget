from database import create_connection, create_table
from transactions import add_transaction, get_transactions, filter_transactions_by_type

def display_menu():
    print("\n--- Budget Tracker ---")
    print("1. Add Transaction")
    print("2. View All Transactions")
    print("3. Filter Transactions by Type (income/expense)")
    print("4. Filter Transactions by Date Range")
    print("5. Exit")

def add_transaction_ui(conn):
    print("\n--- Add New Transaction ---")
    type = input("Enter transaction type (income/expense): ").lower()
    category = input("Enter transaction category (e.g., groceries, rent, etc.): ")
    amount = float(input("Enter transaction amount: "))
    date = input("Enter transaction date (YYYY-MM-DD): ")

    transaction = (type, category, amount, date)
    transaction_id = add_transaction(conn, transaction)
    print(f"\nTransaction added with ID: {transaction_id}")

def view_transactions_ui(conn):
    print("\n--- All Transactions ---")
    transactions = get_transactions(conn)
    
    if not transactions:
        print("No transactions found.")
        return
    
    # displays the transactions
    for t in transactions:
        print(f"ID: {t[0]}, Type: {t[1]}, Category: {t[2]}, Amount: {t[3]}, Date: {t[4]}")

def filter_transactions_ui(conn):
    print("\n--- Filter Transactions by Type ---")
    transaction_type = input("Enter transaction type (income/expense): ").lower()

    # input validation
    if transaction_type not in ['income', 'expense']:
        print("Invalid transaction type. Please enter 'income' or 'expense'.")
        return

    filtered_transactions = filter_transactions_by_type(conn, transaction_type)

    # loops through and displays returned transactions
    if filtered_transactions:
        print("\n--- Filtered Transactions ---")
        for transaction in filtered_transactions:
            print(f"ID: {transaction[0]}, Type: {transaction[1]}, Category: {transaction[2]}, Amount: {transaction[3]}, Date: {transaction[4]}")
    else:
        print(f"No transactions found for type: {transaction_type}")

def main():
    database = "budget_tracker.db"
    conn = create_connection(database)

    if conn is None:
        print("Error! Unable to connect to the database.")
        return

    create_table(conn)

    while True:
        display_menu()
        choice = input("\nChoose an option (1, 2, 3, or 4): ")

        if choice == '1':
            add_transaction_ui(conn)
        elif choice == '2':
            view_transactions_ui(conn)
        elif choice == '3':
            filter_transactions_ui(conn)
        elif choice == '4': 
            print("\nExiting the application.")
            break
        else:
            print("\nInvalid option. Please choose again.")

if __name__ == "__main__":
    main()