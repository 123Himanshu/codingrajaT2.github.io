import csv
import os
from datetime import datetime

# Constants
TRANSACTIONS_FILE = 'transactions.csv'
CATEGORIES = {
    'Income': '💰',
    'Groceries': '🛒',
    'Utilities': '💡',
    'Transportation': '🚗',
    'Entertainment': '🎮',
    'Health': '💊',
    'Education': '📚',
    'Savings': '💲',
    'Other': '💸'
}

# Fixed exchange rate (for illustration purposes)
USD_TO_INR_EXCHANGE_RATE = 75.0  # Replace with the actual exchange rate


# Transaction Class
class Transaction:
    def __init__(self, date, category, description, amount):
        self.date = date
        self.category = category
        self.description = description
        self.amount = amount


# Data Persistence
def save_transactions(transactions):
    with open(TRANSACTIONS_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Date', 'Category', 'Description', 'Amount'])
        writer.writeheader()
        for transaction in transactions:
            writer.writerow({
                'Date': transaction.date,
                'Category': transaction.category,
                'Description': transaction.description,
                'Amount': transaction.amount
            })


def load_transactions():
    if os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            transactions = [Transaction(
                date=row['Date'],
                category=row['Category'],
                description=row['Description'],
                amount=float(row['Amount'])
            ) for row in reader]
        return transactions
    else:
        return []


# Main Application
class BudgetTracker:
    def __init__(self):
        self.transactions = load_transactions()

    def add_income(self, category, amount_in_inr):
        amount_in_usd = amount_in_inr / USD_TO_INR_EXCHANGE_RATE
        self.transactions.append(Transaction(datetime.now().strftime('%Y-%m-%d'), category, '', amount_in_usd))
        save_transactions(self.transactions)

    def add_expense(self, description, amount_in_inr):
        date = datetime.now().strftime('%Y-%m-%d')
        print("Expense Categories:")
        for cat, emoji in CATEGORIES.items():
            print(f"{emoji} {cat}")
        while True:
            category = input("Enter the expense category: ")
            if category in CATEGORIES:
                break
            else:
                print("Invalid category. Please choose from the provided categories.")

        amount_in_usd = amount_in_inr / USD_TO_INR_EXCHANGE_RATE
        self.transactions.append(Transaction(date, category, description, amount_in_usd))
        save_transactions(self.transactions)

    def remove_all_transactions(self):
        self.transactions = []  # Clear all transactions
        save_transactions(self.transactions)

    def calculate_budget(self):
        total_income = sum(transaction.amount for transaction in self.transactions if transaction.category != 'Income')
        total_expense = sum(transaction.amount for transaction in self.transactions if transaction.category == 'Income')
        budget = total_income - total_expense
        return budget

    def analyze_expenses(self):
        categories = {}
        for transaction in self.transactions:
            if transaction.category != 'Income':
                if transaction.category in categories:
                    categories[transaction.category] += transaction.amount
                else:
                    categories[transaction.category] = transaction.amount
        return categories

    def clear_inputs(self):
        pass  # You can implement this if needed


if __name__ == "__main__":
    budget_tracker = BudgetTracker()

    while True:
        title = "💼 Budget Tracker Console Application 💼"
        print(title.center(50, '💰'))

        print("1. Add 💵 Income")
        print("2. Add 💸 Expense")
        print("3. Remove All Transactions")
        print("4. Calculate 💰 Budget")
        print("5. Analyze 💡 Expenses")
        print("6. Show Expense Categories")
        print("7. Exit")

        choice = input("Select an option (1/2/3/4/5/6/7): ")

        if choice == '1':
            category = input("Enter the income category: ")
            amount_in_inr = float(input("Enter the income amount (in INR): "))
            budget_tracker.add_income(category, amount_in_inr)
            print("Income added. 💵")
        elif choice == '2':
            description = input("Enter the expense description: ")
            amount_in_inr = float(input("Enter the expense amount (in INR): "))
            budget_tracker.add_expense(description, amount_in_inr)
            print("Expense added. 💸")
        elif choice == '3':
            budget_tracker.remove_all_transactions()
            print("All transactions removed. 💰")
        elif choice == '4':
            budget = budget_tracker.calculate_budget()
            print(f"Current 💰 Budget: ₹{budget:.2f}")
        elif choice == '5':
            expense_categories = budget_tracker.analyze_expenses()
            print("Expense Analysis: 💡")
            for category, amount in expense_categories.items():
                emoji = CATEGORIES.get(category, '💸')  # Default to money bag emoji if category not found
                print(f"{emoji} {category}: ₹{amount:.2f}")
        elif choice == '6':
            print("Expense Categories:")
            for category, emoji in CATEGORIES.items():
                print(f"{emoji} {category}")
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please select a valid option. 💼")
