import click
from bank_app import AccountHolder, Account, SavingsAccount, CheckingAccount

@click.group()
def cli():
    """CLI Bank Application"""
    pass

@cli.command()
@click.argument('name')
def create_account_holder(name):
    """Create a new account holder."""
    account_holder = AccountHolder.create_account_holder(name)
    click.echo(f"Account holder {name} created with ID {account_holder.id}.")

@cli.command()
@click.argument('name')
def login(name):
    """Login as an account holder."""
    account_holder = AccountHolder.get_account_holder_by_name(name)
    if account_holder:
        click.echo(f"Welcome, {account_holder.name}!")
        manage_account_holder(account_holder)
    else:
        click.echo("Account holder not found. Please create an account holder first.")

def manage_account_holder(account_holder):
    while True:
        click.echo("\n1. Create Savings Account")
        if not account_holder.has_account_type('checking'):
            click.echo("2. Create Checking Account")
        click.echo("3. Deposit Funds")
        click.echo("4. Withdraw Funds")
        click.echo("5. Check Balance")
        click.echo("6. Apply Interest (Savings Account Only)")
        click.echo("7. Logout")
        user_choice = click.prompt("Enter your choice", type=int)

        if user_choice == 1:
            initial_deposit = click.prompt("Enter initial deposit for savings account", type=float)
            account = Account.create_account(account_holder.id, 'savings', initial_deposit)
            click.echo(f"Savings account created with number {account.account_number}.")
        elif user_choice == 2 and not account_holder.has_account_type('checking'):
            initial_deposit = click.prompt("Enter initial deposit for checking account", type=float)
            account = Account.create_account(account_holder.id, 'checking', initial_deposit)
            click.echo(f"Checking account created with number {account.account_number}.")
        elif user_choice == 3:
            account_number = click.prompt("Enter account number to deposit to")
            account = Account.get_account_by_number(account_number)
            if account:
                amount = click.prompt("Enter amount to deposit", type=float)
                account.deposit(amount)
            else:
                click.echo("Account not found.")
        elif user_choice == 4:
            account_number = click.prompt("Enter account number to withdraw from")
            account = Account.get_account_by_number(account_number)
            if account:
                amount = click.prompt("Enter amount to withdraw", type=float)
                account.withdraw(amount)
            else:
                click.echo("Account not found.")
        elif user_choice == 5:
            account_number = click.prompt("Enter account number to check balance")
            account = Account.get_account_by_number(account_number)
            if account:
                account.check_balance()
            else:
                click.echo("Account not found.")
        elif user_choice == 6:
            account_number = click.prompt("Enter account number to apply interest")
            account = Account.get_account_by_number(account_number)
            if isinstance(account, SavingsAccount):
                account.apply_interest()
            else:
                click.echo("Interest can only be applied to savings accounts.")
        elif user_choice == 7:
            break
        else:
            click.echo("Invalid choice. Please choose a valid option.")

if __name__ == '__main__':
    cli()
