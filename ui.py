from database import create_connection

def main():
    database = "budget_tracker.db"
    conn = create_connection(database)

    if conn is None:
        print("Error! Unable to connect to the database.")
        return


# 1 = add
# 2 = view
# 3 = exit

    while True:
        # display_menu()
        choice = input("\nChoose an option (1-3): ")

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