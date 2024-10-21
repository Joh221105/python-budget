import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QDialog, QFormLayout, QLineEdit
from database import create_connection, create_table
from transactions import (
    add_transaction,
    get_transactions,
    filter_transactions_by_type,
    filter_transactions_by_date_range,
    delete_transaction_by_id,
    update_transaction,
    get_transaction_by_id,
    export_to_csv,
)

class BudgetTrackerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Budget Tracker")

         # Initialize the database connection
        self.conn = create_connection("budget_tracker.db")
        create_table(self.conn)  # Make sure the table is created

        # create buttons for menu display
        self.add_transaction_button = QPushButton("Add Transaction")
        self.view_transactions_button = QPushButton("View Transactions")
        self.filter_by_type_button = QPushButton("Filter by Type")
        self.filter_by_date_button = QPushButton("Filter by Date Range")
        self.delete_transaction_button = QPushButton("Delete Transaction")
        self.edit_transaction_button = QPushButton("Edit Transaction")
        self.export_button = QPushButton("Export to CSV")
        self.exit_button = QPushButton("Exit")

        # connects button to respective functions
        self.add_transaction_button.clicked.connect(self.add_transaction_ui)
        self.view_transactions_button.clicked.connect(self.view_transactions_ui)
        self.filter_by_type_button.clicked.connect(self.filter_transactions_ui)
        self.filter_by_date_button.clicked.connect(self.filter_transactions_by_date_range_ui)
        self.delete_transaction_button.clicked.connect(self.delete_transaction_ui)
        self.edit_transaction_button.clicked.connect(self.edit_transaction_ui)
        self.export_button.clicked.connect(self.export_transactions_ui)
        self.exit_button.clicked.connect(self.close)

        # layout of buttons
        layout = QVBoxLayout()
        layout.addWidget(self.add_transaction_button)
        layout.addWidget(self.view_transactions_button)
        layout.addWidget(self.filter_by_type_button)
        layout.addWidget(self.filter_by_date_button)
        layout.addWidget(self.delete_transaction_button)
        layout.addWidget(self.edit_transaction_button)
        layout.addWidget(self.export_button)
        layout.addWidget(self.exit_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

#--------------------------------------------- ADD AND SUBMIT TRANSACTIONS ----------------------------------

    def add_transaction_ui(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Transaction")

        layout = QFormLayout(dialog)

        type_input = QLineEdit(dialog)
        category_input = QLineEdit(dialog)
        amount_input = QLineEdit(dialog)
        date_input = QLineEdit(dialog)
        notes_input = QLineEdit(dialog)

        layout.addRow("Type (income/expense):", type_input)
        layout.addRow("Category:", category_input)
        layout.addRow("Amount:", amount_input)
        layout.addRow("Date (YYYY-MM-DD):", date_input)
        layout.addRow("Notes: ", notes_input)

        button = QPushButton("Add Transaction", dialog)
        layout.addWidget(button)

        button.clicked.connect(lambda: self.submit_add_transaction(
            type_input.text(), category_input.text(),
            float(amount_input.text()), date_input.text(), notes_input.text(), dialog))

        dialog.exec_()

    def submit_add_transaction(self, transaction_type, category, amount, date, notes, dialog):
        transaction = (transaction_type, category, amount, date, notes)
        transaction_id = add_transaction(self.conn, transaction)
        QMessageBox.information(self, "Transaction Added!", f"Transaction ID: {transaction_id}")
        dialog.accept()

# ---------------------------------------- VIEW TRANSACTIONS -------------------------------------------

    def view_transactions_ui(self):
        transactions = get_transactions(self.conn)  

        if not transactions:
            QMessageBox.information(self, "View Transactions", "No transactions found.")
            return

        # formatted string display of transactions
        transaction_list = "\n".join([f"ID: {t[0]}, Type: {t[1]}, Category: {t[2]}, Amount: {t[3]}, Date: {t[4]}, Notes: {t[5]}" for t in transactions])

        # shows the fetched transaction in message box
        QMessageBox.information(self, "View Transactions", transaction_list)

    def filter_transactions_ui(self):
        QMessageBox.information(self, "Filter Transactions by Type", "Placeholder")

    def filter_transactions_by_date_range_ui(self):
        QMessageBox.information(self, "Filter Transactions by Date Range", "Placeholder")

    def delete_transaction_ui(self):
        QMessageBox.information(self, "Delete Transaction", "Placeholder")

    def edit_transaction_ui(self):
        QMessageBox.information(self, "Edit Transaction", "Placeholder")

    def export_transactions_ui(self):
        QMessageBox.information(self, "Export Transactions", "Placeholder")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BudgetTrackerApp()
    window.show()
    sys.exit(app.exec_())
