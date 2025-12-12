from PyQt6.QtWidgets import *
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from gui import Ui_MainWindow
from accounts import Account, SavingAccount
from login_ui import Ui_Dialog

class Logic(QMainWindow, Ui_MainWindow):
    """Main Application Window

    Handles user input, account creations, and transactions"""
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.accounts = []
        self.selected_account = None

        self.model = QStandardItemModel()
        self.listView_updates.setModel(self.model)

        self.pushButton_create_account.clicked.connect(self.create_account)
        self.pushButton.clicked.connect(self.create_saving_account)
        self.pushButton_deposit.clicked.connect(self.deposit)
        self.pushButton_withdraw.clicked.connect(self.withdraw)
        self.pushButton_delete_account.clicked.connect(self.delete_account)
        self.pushButton_set_balance.clicked.connect(self.set_balance)
        self.listWidget_accounts.itemClicked.connect(self.select_account)

    def select_account(self, item: QListWidgetItem) -> None:
        """Sets the current account in accordance with user selection"""
        self.selected_account = item.data(QtCore.Qt.ItemDataRole.UserRole)
        self.update_account_view()

    def update_account_list(self) -> None:
        """Refreshes the account display with current account information"""
        self.listWidget_accounts.clear()
        for acc in self.accounts:
            acc_type = "SavingAccount" if isinstance(acc, SavingAccount) else "Account"
            item_text = f"{acc.get_name()} ({acc_type}) : ${acc.get_balance():.2f}"
            item = QListWidgetItem(item_text)
            item.setData(QtCore.Qt.ItemDataRole.UserRole, acc) # Links QListWidgetItem to the Account object using UserRole
            color = QtCore.Qt.GlobalColor.blue if isinstance(acc, SavingAccount) else QtCore.Qt.GlobalColor.black
            item.setForeground(QtGui.QBrush(color))
            self.listWidget_accounts.addItem(item)

    def update_account_view(self) -> None:
        """Sets the account display with account information for selected account"""
        self.model.clear()
        if not self.selected_account:
            return

        for entry in getattr(self.selected_account, 'activity_log', []):
            item = QStandardItem(entry)
            item.setEditable(False)
            self.model.appendRow(item)

        if self.model.rowCount() > 0:
            index = self.model.index(self.model.rowCount() - 1, 0)
            self.listView_updates.scrollTo(index)

    def create_account(self) -> None:
        """Creates an account using the Account class from the accounts file"""
        name, ok = QInputDialog.getText(self, "Create Account", "Enter name:")
        if ok and name:
            acc = Account(name)
            acc.activity_log = [f"Account '{name}' created."]
            self.accounts.append(acc)
            self.update_account_list()

    def create_saving_account(self) -> None:
        """Creates an account using the SavingAccount class from the accounts file"""
        name, ok = QInputDialog.getText(self, "Create SavingAccount", "Enter name:")
        if ok and name:
            acc = SavingAccount(name)
            acc.activity_log = [f"SavingAccount '{name}' created."]
            self.accounts.append(acc)
            self.update_account_list()

    def deposit(self) -> None:
        """Calls the deposit function from the accounts file and updates the account display"""
        if not self.selected_account:
            QMessageBox.warning(self, "Error", "Please select an account first")
            return

        amount, ok = QInputDialog.getDouble(self, "Deposit", "Enter amount:", min = 0.01, max = 1000000, decimals=2)

        if not ok:
            return

        self.selected_account.deposit(amount)
        self.selected_account.activity_log.append(f"Deposited ${amount:.2f}. Balance: ${self.selected_account.get_balance():.2f}")
        self.update_account_list()
        self.update_account_view()

    def withdraw(self) -> None:
        """Calls the withdraw function from the accounts file and updates the account display"""
        if not self.selected_account:
            QMessageBox.warning(self, "Error", "Please select an account first")
            return

        amount, ok = QInputDialog.getDouble(self, "Withdraw", "Enter amount:", min = 0.01, max = 1000000, decimals=2)

        if not ok:
            return

        if not self.selected_account.withdraw(amount):
            QMessageBox.warning(self, "Error", "Insufficient funds")
            return

        self.selected_account.activity_log.append(f"Withdrew ${amount:.2f}. Balance: ${self.selected_account.get_balance():.2f}")
        self.update_account_list()
        self.update_account_view()

    def set_balance(self) -> None:
        """Sets the balance of the selected account"""
        if not self.selected_account:
            QMessageBox.warning(self, "Error", "Please select an account first")
            return
        amount, ok = QInputDialog.getDouble(self, "Set Balance", "Enter new balance:", min = .01, max = 1000000, decimals = 2)

        if not ok:
            return

        if isinstance(self.selected_account, SavingAccount):
            if amount < SavingAccount.minimum:
                QMessageBox.warning(self, "Error", f"Saving Account balance cannot be lower than {SavingAccount.minimum}")
                return
        elif isinstance(self.selected_account, Account):
            if amount < 0:
                QMessageBox.warning(self, "Error", "Saving Account balance cannot be less than 0")
                return

        old_balance = self.selected_account.get_balance()
        self.selected_account.set_balance(amount)
        self.selected_account.activity_log.append(f"Balance changed from ${old_balance:.2f} to ${amount:.2f}")
        self.update_account_list()
        self.update_account_view()

    def delete_account(self) -> None:
        """Removes the selected account from the account list"""
        if not self.selected_account:
            QMessageBox.warning(self, "Error", "Please select an account first")
            return
        if self.selected_account in self.accounts:
            self.accounts.remove(self.selected_account)
            self.selected_account = None
            self.update_account_list()
            self.update_account_view()

class LoginDialog(QDialog, Ui_Dialog):
    """Login Window

    Validates a username and password"""
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.pushButton_login.clicked.connect(self.validate)
        self.pushButton_cancel.clicked.connect(self.reject)

    def validate(self) -> None:
        """Checks to make sure the username and password are valid"""

        username = self.lineEdit_username.text().strip()
        password = self.lineEdit_password.text().strip()

        if username == 'admin' and password == 'password':
            self.accept()
        else:
            QMessageBox.warning(self, 'Login Failed', 'Invalid Credentials')