import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox

class BudgetTrackerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Budget Tracker")

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

    def add_transaction_ui(self):
        QMessageBox.information(self, "Add Transaction", "Placeholder")

    def view_transactions_ui(self):
        QMessageBox.information(self, "View Transactions", "Placeholder")

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
