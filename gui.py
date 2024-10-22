import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox, QDialog, QFormLayout, QLineEdit, QTableWidget, QTableWidgetItem, QLabel, QFileDialog
from database import create_connection, create_table
from datetime import datetime
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
        self.view_transactions_button = QPushButton("View All Transactions")
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
        self.filter_by_date_button.clicked.connect(self.show_date_range_input)
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
        QMessageBox.information(self, "Transaction Added!", f"Transaction Added. Transaction ID: {transaction_id}")
        dialog.accept()

# ---------------------------------------- VIEW TRANSACTIONS -------------------------------------------

    def view_transactions_ui(self):
        transactions = get_transactions(self.conn)  

        dialog = QDialog(self)
        dialog.setWindowTitle("All Transactions")

        dialog.setGeometry(100, 100, 1000, 500) # sets initial size of transactions table
        
        # creates table to display transactions
        table = QTableWidget(dialog)
        table.setColumnCount(6)  #  designates number of columns
        table.setHorizontalHeaderLabels(["ID", "Type", "Category", "Amount", "Date", "Notes"]) # column names
        table.setColumnWidth(5, 400) # sets the 6th column - Notes to be 400 pixels
        
        # set the number of rows in the table to number of transactions
        table.setRowCount(len(transactions))
        table.setSortingEnabled(True)

        # populate table with data
        for row, transaction in enumerate(transactions):
            for column, value in enumerate(transaction):
                table.setItem(row, column, QTableWidgetItem(str(value)))  # values needs to be converted to strings to be displayed

        layout = QVBoxLayout()
        layout.addWidget(table)
        dialog.setLayout(layout)
        
        dialog.exec_()

# -------------------------------FILTER TRANSACTIONS BY TYPE ----------------------------------------------------

    def filter_transactions_ui(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Filter Transactions by Type")

        layout = QVBoxLayout()

        # Label and Input field for transaction type
        label = QLabel("Enter transaction type (income/expense):", dialog)
        layout.addWidget(label)

        type_input = QLineEdit(dialog)
        layout.addWidget(type_input)

        # creates button to submit input
        submit_button = QPushButton("Submit", dialog)
        layout.addWidget(submit_button)

        submit_button.clicked.connect(lambda: self.show_filtered_transactions(type_input.text().lower(), dialog))

        dialog.setLayout(layout)
        dialog.exec_()

    def show_filtered_transactions(self, transaction_type, parent_dialog):
        # validates input
        if transaction_type not in ['income', 'expense']:
            QMessageBox.warning(self, "Invalid Input", "Please enter 'income' or 'expense'.")
            return

        # retrieves filtered transactions from the database
        filtered_transactions = filter_transactions_by_type(self.conn, transaction_type)

        parent_dialog.close()

        # creates a new dialog to display filtered transactions
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Filtered Transactions - {transaction_type.capitalize()}")

        dialog.resize(800, 400)

        # creates table to display transactions
        table = QTableWidget(dialog)
        table.setColumnCount(6) 
        table.setHorizontalHeaderLabels(["ID", "Type", "Category", "Amount", "Date", "Notes"])
        table.setRowCount(len(filtered_transactions))

        table.setSortingEnabled(True)

        # populates table with filtered results
        for row, transaction in enumerate(filtered_transactions):
            for column, value in enumerate(transaction):
                table.setItem(row, column, QTableWidgetItem(str(value)))

        # sets notes column width
        table.setColumnWidth(5, 400)

        layout = QVBoxLayout()
        layout.addWidget(table)
        dialog.setLayout(layout)

        dialog.exec_()

# --------------------------FILTER TRANSACTIONS BY DATE RANGE -------------------------------------

    def show_date_range_input(self):

        dialog = QDialog(self)
        dialog.setWindowTitle("Filter Transactions by Date Range")

        # user adds start date and end date fields 
        start_date_label = QLabel("Start Date (YYYY-MM-DD):")
        self.start_date_input = QLineEdit()
        
        end_date_label = QLabel("End Date (YYYY-MM-DD):")
        self.end_date_input = QLineEdit()

        # adds submit button
        submit_button = QPushButton("Submit")

        # layout for date inputs and submit button
        layout = QFormLayout()
        layout.addRow(start_date_label, self.start_date_input)
        layout.addRow(end_date_label, self.end_date_input)
        layout.addWidget(submit_button)

        dialog.setLayout(layout)

        # connects the submit button to function that fetches filtered transactions, passes start and end date and dialog
        submit_button.clicked.connect(lambda: self.show_filtered_transactions_by_date(self.start_date_input.text(), self.end_date_input.text(), dialog))

        dialog.exec_()
    
    def show_filtered_transactions_by_date(self, start_date, end_date, parent_dialog):

        # close the input dialog / parent dialog
        parent_dialog.close()

        # validate date formats
        try:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
            
            if start_date_obj > end_date_obj:
                QMessageBox.warning(self, "Invalid Date Range", "Start date cannot be later than end date.")
                return

        except ValueError:
            # shows warning if the date format is incorrect
            QMessageBox.warning(self, "Invalid Date Format", "Please enter dates in YYYY-MM-DD format.")
            return

        # fetches the filtered transactions from the database
        transactions = filter_transactions_by_date_range(self.conn, start_date, end_date)

        # displays the filtered transactions in table

        dialog = QDialog(self)
        dialog.setWindowTitle(f"Filtered Transactions from {start_date} to {end_date}")

        dialog.resize(800, 400)

        # creates table to display filtered results
        table = QTableWidget(dialog)
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(["ID", "Type", "Category", "Amount", "Date", "Notes"])
        table.setRowCount(len(transactions))
        table.setSortingEnabled(True)

        for row, transaction in enumerate(transactions):
            for column, value in enumerate(transaction):
                table.setItem(row, column, QTableWidgetItem(str(value)))

        table.setColumnWidth(5, 400)

        layout = QVBoxLayout()
        layout.addWidget(table)
        dialog.setLayout(layout)

        dialog.exec_()
            
# --------------------------------------- DELETE TRANSACTION BY ID --------------------------------------------
    def delete_transaction_ui(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Delete Transaction")

        # creates label and input field for transaction ID
        transaction_id_label = QLabel("Enter Transaction ID to Delete:")
        transaction_id_input = QLineEdit()

        # creates submit button
        submit_button = QPushButton("Delete")

        # lays out the display of the widgets
        layout = QFormLayout()
        layout.addRow(transaction_id_label, transaction_id_input)
        layout.addWidget(submit_button)
        dialog.setLayout(layout)

        # connects submit button to delete function
        submit_button.clicked.connect(lambda: self.delete_transaction(transaction_id_input.text(), dialog))

        dialog.exec_()

    def delete_transaction(self, id, parent_dialog):
        # validates id input
        try:
            transaction_id = int(id)  # converts id to integer
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid transaction ID.")
            return

        # calls function to delete transaction by id, returns bool
        success = delete_transaction_by_id(self.conn, transaction_id)

        parent_dialog.close()

        # shows success or failure message
        if success:
            QMessageBox.information(self, "Success", f"Transaction with ID {transaction_id} has been deleted.")
        else:
            QMessageBox.warning(self, "Failure", f"No transaction found with ID {transaction_id}.")

# --------------------------------------- EDIT TRANSACTION BY ID ------------------------------------------------
    def edit_transaction_ui(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Transaction")

        instruction_label = QLabel("Blank = Remain Same")
        instruction_label.setStyleSheet("font-weight: bold; font-size: 12px;")

        # creates label and input fields for each column
        transaction_id_label = QLabel("Enter Transaction ID to Edit:")
        transaction_id_input = QLineEdit()

        # Create input fields for new transaction values
        type_label = QLabel("Type (income/expense):")
        type_input = QLineEdit()

        category_label = QLabel("Category:")
        category_input = QLineEdit()

        amount_label = QLabel("Amount:")
        amount_input = QLineEdit()

        date_label = QLabel("Date (YYYY-MM-DD):")
        date_input = QLineEdit()

        notes_label = QLabel("Notes:")
        notes_input = QLineEdit()

        submit_button = QPushButton("Update")

        # display loyout
        layout = QFormLayout()
        layout.addWidget(instruction_label)
        layout.addRow(transaction_id_label, transaction_id_input)
        layout.addRow(type_label, type_input)
        layout.addRow(category_label, category_input)
        layout.addRow(amount_label, amount_input)
        layout.addRow(date_label, date_input)
        layout.addRow(notes_label, notes_input)
        layout.addWidget(submit_button)

        dialog.setLayout(layout)

        # connects submit button to update function
        submit_button.clicked.connect(lambda: self.update_transaction_by_id(transaction_id_input.text(), type_input.text(), category_input.text(), amount_input.text(), date_input.text(), notes_input.text(), dialog))

        dialog.exec_()

    def update_transaction_by_id(self, transaction_id_str, transaction_type, category, amount_str, date, notes, parent_dialog):
    
        # validates user id
        try:
            transaction_id = int(transaction_id_str)
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid transaction ID.")
            return
        
        # gets the transaction with associated id
        current_transaction = get_transaction_by_id(self.conn, transaction_id)    
        if not current_transaction:
            QMessageBox.warning(self, "Transaction Not Found", f"No transaction found with ID {transaction_id}.")
            return    

        # validates amount 
        amount = float(amount_str) if amount_str else current_transaction[3]

        # creates a tuple with updated values (using previous/existing values if input is empty)
        updated_transaction = (
            transaction_type or current_transaction[1], 
            category or current_transaction[2],            
            amount,                                        
            date or current_transaction[4],                
            notes or current_transaction[5]                
        )    

        # calls function in transactions.py to update transaction
        success = update_transaction(self.conn, transaction_id, updated_transaction)

        parent_dialog.close()

        # shows success or failure message
        if success:
            QMessageBox.information(self, "Success", f"Transaction with ID {transaction_id} has been updated.")
        else:
            QMessageBox.warning(self, "Failure", f"Failed to update transaction with ID {transaction_id}.")

# --------------------------------------- EXPORT TRANSACTIONS TO CSV ---------------------------------------------
    def export_transactions_ui(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)

        if not file_name:
            return  # user cancelled save

        try:
            export_to_csv(self.conn, file_name)
            
            QMessageBox.information(self, "Success", f"Transactions exported to {file_name} successfully.")

        except Exception as e:
            QMessageBox.warning(self, "Export Failed", f"An error occurred while exporting transactions: {str(e)}")


# --------------------------------------- SUMMARIZE TRANSACTIONS -------------------------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BudgetTrackerApp()
    window.show()
    sys.exit(app.exec_())
