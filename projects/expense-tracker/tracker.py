# Import the JSON module so we can read and write data to a JSON file
import json

#function that loads expenses from a JSON file
def load_expenses():
    try:
        with open("expenses.json", "r") as file:
            return json.load(file)
    except:
        return[]

# function that saves expenses to a JSON file
def save_expenses(expenses):
     # Open the file in write mode
     with open ("expenses.json", "w") as file:
         # Write the expenses data to the file in JSON format
         json.dump(expenses, file, indent=4)

#function to add an expense to the list of expenses
def add_expense(expenses):
     # Ask the user to input expense details
    date = input("Enter the date of the expense (YYYY-MM-DD): ")
    amount = float(input("Enter the amount of the expense: "))
    category = input("Enter the category of the expense:")
    description = input("Enter a description of the expense: ")

    # Create a dictionary to represent the expense
    expense = {
        "date": date,
        "amount": amount,
        "category": category,
        "description": description
        }
     # Add the new expense to the list
    expenses.append(expense)
    # Save updated list to the file
    save_expenses(expenses)

    print("Expense added.")

# Function to display all expenses
def view_expenses(expenses):
     # Loop through each expense in the list
     for e in expenses:
         # Print the expense details in a readable format
         print(f"{e['date']} | £{e['amount']} | {e['category']} | {e['description']}")

# Function to show total spending by category
def summary_by_category(expenses):
    # Create a dictionary to hold the total spending for each category
    summary = {}
    # Loop through each expense in the list
    # Loop through each expense
    for e in expenses:

        category = e["category"]
        amount = e["amount"]

        # Add amount to existing category total
        if category in summary:
            summary[category] += amount
        else:
            # Create new category entry
            summary[category] = amount

    # Print the results
    print("\nSpending by category:")
    for category, total in summary.items():
        print(f"{category}: £{total}")

# Main function that runs the CLI program
def main():

    # Load existing expenses when program starts
    expenses = load_expenses()

    # Loop to keep the program running
    while True:

        # Display menu options
        print("\nExpense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. View Summary by Category")
        print("4. Exit")

        # Get user's choice
        choice = input("Choose an option: ")

        # Run the selected feature
        if choice == "1":
            add_expense(expenses)

        elif choice == "2":
            view_expenses(expenses)

        elif choice == "3":
            summary_by_category(expenses)

        elif choice == "4":
            break

        else:
            print("Invalid option. Try again.")


# Ensures the program runs only when executed directly
if __name__ == "__main__":
    main()