import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banksystem.settings')  
django.setup()

from Users.models import User
from Banks.models import Bank, Branch
from Accounts.models import Account

def generate_unique_account_number(bank):
    while True:
        acc_number = str(random.randint(10**9, 10**10 - 1))
        if not Account.objects.filter(account_number=acc_number, branch__bank=bank).exists():
            return acc_number

def populate_accounts():
    users = User.objects.all()[2:]  
    banks = Bank.objects.all()  
    
    for user in users:
        bank = random.choice(banks)
        
        branch_code = random.choice(["001", "002"])
        branch = Branch.objects.get(bank=bank, branch_code=branch_code)
        
        account_number = generate_unique_account_number(bank)
        Account.objects.create(
            account_number=account_number,
            user=user,
            branch=branch,
            balance=random.uniform(1000.00, 10000.00),  
            account_type=random.choice(['savings', 'current']),
        )
        
        print(f"Created account for {user.username} with account number {account_number}")

if __name__ == '__main__':
    populate_accounts()
