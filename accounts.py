"""
This file creates Account and Saving Account classes for the bank app

This file contains logic to deposit, withdraw, set a balance for both accounts.

Logic to apply interest is also included, but only applies to the Saving Account class
"""

class Account:
    """Creates a standard account with the ability to deposit, withdraw, set a balance, set a name, get the balance, and get the name"""
    def __init__(self, name, balance = 0):
        self.__name = name
        self.__balance = balance
        self.set_balance(self.__balance)
        self.__history = []

    def deposit(self, amount):
        """Deposit a positive amount into the account
        :param amount: The amount to deposit
        :return: True if deposit was successful, False otherwise
        """
        if amount > 0:
            self.set_balance(self.get_balance() + amount)
            self.__history.append(f"Deposited ${amount:.2f}")
            return True
        else:
            return False

    def withdraw(self, amount):
        """Withdraw a positive amount from the account if funds are available
        :param amount: The amount to withdraw
        :return: True if withdraw was successful, False otherwise"""
        if amount > 0:
            if self.get_balance() - amount < 0:
                return False
            self.set_balance(self.get_balance() - amount)
            self.__history.append(f"Withdrew ${amount:.2f}")
            return True
        else:
            return False

    def get_balance(self):
        """Get the balance of the account"""
        return self.__balance

    def get_name(self):
        """Get the name of the account"""
        return self.__name

    def set_balance(self, value):
        """Set the balance of the account to a non-negative number
        :param value: The balance to set"""
        if value < 0:
            self.__balance = 0
            self.__history.append(f"Balance set to ${value:.2f}")
        else:
            self.__balance = value

    def set_name(self, value):
        """Set the name of the account"""
        self.__name = value

    def __str__(self):
        return f'Account name: {self.get_name()}, Account balance: {self.get_balance():.2f}'

class SavingAccount(Account):
    """An account with a minimum balance and an interest accrual function"""
    minimum = 100
    rate = 0.02

    def __init__(self, name):
        super().__init__(name, SavingAccount.minimum)
        self.__deposit_count = 0

    def apply_interest(self):
        """Applies the interest accrual function to the saving account"""
        Account.set_balance(self, (Account.get_balance(self) * (1 + self.rate)))

    def deposit(self, amount):
        """Deposit a positive amount into the account. Once five deposits are made the apply_interest function is called
        :param amount: The amount to deposit
        :return: True if deposit was successful, False otherwise"""
        if super().deposit(amount):
            self.__deposit_count += 1
            if self.__deposit_count >= 5:
                self.apply_interest()
                self.__deposit_count = 0
            return True
        else:
            return False

    def withdraw(self, amount):
        """Withdraw a positive amount from the account if funds are available and the balance would not drop below the minimum
        :param amount: The amount to withdraw
        :return: True if withdraw was successful, False otherwise"""
        if amount > 0:
            if (Account.get_balance(self) - amount) < self.minimum:
                return False
            Account.set_balance(self, Account.get_balance(self) - amount)
            return True
        else:
            return False

    def set_balance(self, value):
        """Set the balance of the account to a non-negative number
        :param value: The balance to set"""
        if value < self.minimum:
            Account.set_balance(self, self.minimum)
        else:
            Account.set_balance(self, value)

    def __str__(self):
        return f'SAVING ACCOUNT: ' + super().__str__()