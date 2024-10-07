from database import create_connection

def display_menu():
    print("\n--- Budget Tracker ---")
    print("1. Add Transaction")
    print("2. View All Transactions")
    print("3. Exit")

def main():
    database = "budget_tracker.db"
    conn = create_connection(database)

    if conn is None:
        print("Error! Unable to connect to the database.")
        return


    while True:
        display_menu()
        choice = input("\nChoose an option (1, 2, or 3): ")

        # Placeholder for options
        if choice == '1':
            pass
        elif choice == '2':
            pass
        elif choice == '3':
            print("\nExiting the application.")
            break
        else:
            print("\nInvalid option. Please choose again.")

if __name__ == "__main__":
    main()