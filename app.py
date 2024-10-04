from database import create_connection
from ui import main_menu

def main():
    conn = create_connection('budget_tracker.db')
    main_menu(conn)
    conn.close()

if __name__ == "__main__":
    main()