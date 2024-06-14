# CLI Bank Application

This is a command-line interface (CLI) bank application that allows users to create accounts, deposit and withdraw funds, and manage checking and savings accounts. The application utilizes SQLite for database management.

## Features

- **Create Account Holder**: Register a new account holder.
- **Create Accounts**: Create checking and savings accounts with a specified initial deposit.
- **Deposit Funds**: Add funds to an account.
- **Withdraw Funds**: Withdraw funds from an account, with overdraft support for checking accounts.
- **Check Balance**: View the balance of any account.
- **Apply Interest**: Automatically apply interest to savings accounts.
- **Total Balance**: Check the total balance across all accounts for an account holder.

## Prerequisites

- Python 3.x
- SQLite

## Installation

1. Clone the repository:

   ```sh
   git clone
   cd cli-bank-app
   ```

2. Create a virtual environment:

   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:

   ```sh
   pip install -r requirements.txt
   ```

## Setup

1. Initialize the database:

   The `db_setup.py` script will automatically create the required tables in the `bank.db` SQLite database file.

2. Run the CLI:

   ```sh
   python cli.py
   ```

## Usage

1. **Create a New Account Holder:**

   ```sh
   python cli.py create-account-holder "John Doe"
   ```

2. **Login as an Account Holder:**

   ```sh
   python cli.py login "John Doe"
   ```

   After logging in, you can manage accounts and perform transactions through the interactive prompts.

## Commands

- `create-account-holder [name]`: Create a new account holder.
- `login [name]`: Login as an account holder.

## Example Workflow

1. Create a new account holder:

   ```sh
   python cli.py create-account-holder "John Doe"
   ```

2. Login as the account holder:

   ```sh
   python cli.py login "John Doe"
   ```

3. Follow the prompts to create accounts, deposit/withdraw funds, and check balances.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
