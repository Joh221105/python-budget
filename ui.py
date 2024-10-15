from database import create_connection, create_table
from transactions import add_transaction, get_transactions, filter_transactions_by_type, filter_transactions_by_date_range, delete_transaction_by_id, update_transaction

def display_menu():
    print("\n--- Budget Tracker ---")
    print("1. Add Transaction")
    print("2. View All Transactions")
    print("3. Filter Transactions by Type (income/expense)")
    print("4. Filter Transactions by Date Range")
    print("5. Delete Transaction")
    print("6. Exit")

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

def filter_transactions_by_date_range_ui(conn):
    print("\n--- Filter Transactions by Date Range ---")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    filtered_transactions = filter_transactions_by_date_range(conn, start_date, end_date)

    if filtered_transactions:
        print("\n--- Filtered Transactions ---")
        for transaction in filtered_transactions:
            print(f"ID: {transaction[0]}, Type: {transaction[1]}, Category: {transaction[2]}, Amount: {transaction[3]}, Date: {transaction[4]}")
    else:
        print(f"No transactions found between {start_date} and {end_date}")

def delete_transaction_ui(conn):
    print("\n--- Delete Transaction ---")
    transaction_id = int(input("Enter the transaction ID to delete: "))

    success = delete_transaction_by_id(conn, transaction_id)

    if success:
        print(f"Transaction with ID {transaction_id} was deleted successfully.")
    else:
        print(f"No transaction found with ID {transaction_id}.")

def edit_transaction_ui(conn):
    print("\n--- Edit Transaction ---")
    transaction_id = int(input("Enter the transaction ID to edit: "))

    # gathers the fields to be updated and their new values
    new_type = input("Enter new transaction type (income/expense): ").lower()
    new_category = input("Enter new transaction category (e.g., groceries, rent, etc.): ")
    new_amount = float(input("Enter new transaction amount: "))
    new_date = input("Enter new transaction date (YYYY-MM-DD): ")

    # creates tuple of updated values
    updated_transaction = (new_type, new_category, new_amount, new_date)
    
    success = update_transaction(conn, transaction_id, updated_transaction)

    if success:
        print(f"Transaction with ID {transaction_id} was updated successfully.")
    else:
        print(f"No transaction found with ID {transaction_id}.")

def main():
    database = "budget_tracker.db"
    conn = create_connection(database)

    if conn is None:
        print("Error! Unable to connect to the database.")
        return
    
    create_table(conn)

    while True:
        display_menu()
        choice = input("\nChoose an option (1, 2, 3, 4, 5, or 6): ")

        if choice == '1':
            add_transaction_ui(conn)
        elif choice == '2':
            view_transactions_ui(conn)
        elif choice == '3':
            filter_transactions_ui(conn)
        elif choice == '4':
            filter_transactions_by_date_range_ui(conn)
        elif choice == '5':
            delete_transaction_ui(conn)
        elif choice == '6':
            print("\nExiting the application.")
            break

if __name__ == "__main__":
    main()
