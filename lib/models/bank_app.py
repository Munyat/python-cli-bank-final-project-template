import sqlite3
import random
import string
from db_setup import get_connection, create_tables

create_tables()

def generate_account_number(length=10):
    """Generate a random account number of specified length."""
    return ''.join(random.choices(string.digits, k=length))

class AccountHolder:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        total_balance = self.get_total_balance()
        return f"Account Holder: {self.name}, Total Balance: ${total_balance:.2f}"

    def get_total_balance(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT SUM(balance) FROM account WHERE account_holder_id = ?', (self.id,))
        result = cursor.fetchone()[0]
        conn.close()
        return result if result else 0

    def has_account_type(self, account_type):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM account WHERE account_holder_id = ? AND account_type = ?', (self.id, account_type))
        result = cursor.fetchone()[0]
        conn.close()
        return result > 0

    @staticmethod
    def create_account_holder(name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO account_holder (name) VALUES (?)', (name,))
        conn.commit()
        new_holder = AccountHolder(cursor.lastrowid, name)
        conn.close()
        return new_holder

    @staticmethod
    def get_account_holder_by_name(name):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM account_holder WHERE name = ?', (name,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return AccountHolder(result[0], result[1])
        return None

class Account:
    def __init__(self, id, account_number, balance, account_holder_id, account_type):
        self.id = id
        self.account_number = account_number
        self.balance = balance
        self.account_holder_id = account_holder_id
        self.account_type = account_type

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE account SET balance = ? WHERE id = ?', (self.balance, self.id))
            cursor.execute('INSERT INTO "transaction" (account_id, amount, type) VALUES (?, ?, ?)', (self.id, amount, 'deposit'))
            conn.commit()
            conn.close()
            print(f"Deposited ${amount:.2f}. New balance is ${self.balance:.2f}.")
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > 0:
            if self.balance >= amount:
                self.balance -= amount
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute('UPDATE account SET balance = ? WHERE id = ?', (self.balance, self.id))
                cursor.execute('INSERT INTO "transaction" (account_id, amount, type) VALUES (?, ?, ?)', (self.id, -amount, 'withdrawal'))
                conn.commit()
                conn.close()
                print(f"Withdrew ${amount:.2f}. New balance is ${self.balance:.2f}.")
            else:
                print("Insufficient funds.")
        else:
            print("Withdrawal amount must be positive.")

    def check_balance(self):
        print(f"Account {self.account_number} balance is ${self.balance:.2f}.")

    @staticmethod
    def create_account(account_holder_id, account_type, initial_deposit):
        account_number = generate_account_number()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO account (account_number, balance, account_holder_id, account_type) VALUES (?, ?, ?, ?)',
                       (account_number, initial_deposit, account_holder_id, account_type))
        conn.commit()
        new_account = Account(cursor.lastrowid, account_number, initial_deposit, account_holder_id, account_type)
        conn.close()
        return new_account

    @staticmethod
    def get_account_by_number(account_number):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM account WHERE account_number = ?', (account_number,))
        result = cursor.fetchone()
        conn.close()
        if result:
            if result[4] == 'checking':
                return CheckingAccount(result[0], result[1], result[2], result[3])
            elif result[4] == 'savings':
                return SavingsAccount(result[0], result[1], result[2], result[3])
        return None

class CheckingAccount(Account):
    def __init__(self, id, account_number, balance, account_holder_id):
        super().__init__(id, account_number, balance, account_holder_id, 'checking')
        self.overdraft_limit = 100

    def withdraw(self, amount):
        if amount > 0:
            if self.balance + self.overdraft_limit >= amount:
                self.balance -= amount
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute('UPDATE account SET balance = ? WHERE id = ?', (self.balance, self.id))
                cursor.execute('INSERT INTO "transaction" (account_id, amount, type) VALUES (?, ?, ?)', (self.id, -amount, 'withdrawal'))
                conn.commit()
                conn.close()
                print(f"Withdrew ${amount:.2f}. New balance is ${self.balance:.2f}.")
            else:
                print("Insufficient funds, even with overdraft limit.")
        else:
            print("Withdrawal amount must be positive.")

class SavingsAccount(Account):
    def __init__(self, id, account_number, balance, account_holder_id):
        super().__init__(id, account_number, balance, account_holder_id, 'savings')
        self.interest_rate = 0.02

    def apply_interest(self):
        interest = self.balance * self.interest_rate
        self.balance += interest
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE account SET balance = ? WHERE id = ?', (self.balance, self.id))
        cursor.execute('INSERT INTO "transaction" (account_id, amount, type) VALUES (?, ?, ?)', (self.id, interest, 'interest'))
        conn.commit()
        conn.close()
        print(f"Applied ${interest:.2f} interest. New balance is ${self.balance:.2f}.")

def main():
    print("Welcome to the CLI Bank!")
    
    while True:
        print("\n1. Create New Account Holder")
        print("2. Login as Account Holder")
        print("3. Exit")
        main_choice = input("Enter your choice: ")

        if main_choice == '1':
            holder_name = input("Enter the new account holder's name: ")
            account_holder = AccountHolder.create_account_holder(holder_name)
            print(f"Account holder {holder_name} created with ID {account_holder.id}.")
        elif main_choice == '2':
            holder_name = input("Enter the account holder's name: ")
            account_holder = AccountHolder.get_account_holder_by_name(holder_name)
            if account_holder:
                print(f"Welcome, {account_holder.name}!")
                while True:
                    print("\n1. Create Savings Account")
                    if not account_holder.has_account_type('checking'):
                        print("2. Create Checking Account")
                    print("3. Deposit Funds")
                    print("4. Withdraw Funds")
                    print("5. Check Balance")
                    print("6. Apply Interest (Savings Account Only)")
                    print("7. Logout")
                    user_choice = input("Enter your choice: ")

                    if user_choice == '1':
                        initial_deposit = float(input("Enter initial deposit for savings account: "))
                        account = Account.create_account(account_holder.id, 'savings', initial_deposit)
                        print(f"Savings account created with number {account.account_number}.")
                    elif user_choice == '2' and not account_holder.has_account_type('checking'):
                        initial_deposit = float(input("Enter initial deposit for checking account: "))
                        account = Account.create_account(account_holder.id, 'checking', initial_deposit)
                        print(f"Checking account created with number {account.account_number}.")
                    elif user_choice == '3':
                        account_number = input("Enter account number to deposit to: ")
                        account = Account.get_account_by_number(account_number)
                        if account:
                            amount = float(input("Enter amount to deposit: "))
                            account.deposit(amount)
                        else:
                            print("Account not found.")
                    elif user_choice == '4':
                        account_number = input("Enter account number to withdraw from: ")
                        account = Account.get_account_by_number(account_number)
                        if account:
                            amount = float(input("Enter amount to withdraw: "))
                            account.withdraw(amount)
                        else:
                            print("Account not found.")
                    elif user_choice == '5':
                        account_number = input("Enter account number to check balance: ")
                        account = Account.get_account_by_number(account_number)
                        if account:
                            account.check_balance()
                        else:
                            print("Account not found.")
                    elif user_choice == '6':
                        account_number = input("Enter account number to apply interest: ")
                        account = Account.get_account_by_number(account_number)
                        if isinstance(account, SavingsAccount):
                            account.apply_interest()
                        else:
                            print("Interest can only be applied to savings accounts.")
                    elif user_choice == '7':
                        break
                    else:
                        print("Invalid choice. Please choose a valid option.")
            else:
                print("Account holder not found. Please create an account holder first.")
        elif main_choice == '3':
            print("Thank you for using CLI Bank. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()
