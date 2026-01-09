def add_expense():
    amount = input("Enter amount: ")
    category = input("Enter category: ")
    note = input("Enter note: ")

    with open("expenses.txt", "a") as f:
        f.write(amount + "," + category + "," + note + "\n")

    print("Expense added successfully!\n")


def view_expenses():
    try:
        with open("expenses.txt", "r") as f:
            print("\n--- All Expenses ---")
            for line in f:
                data = line.strip().split(",")
                print("Amount:", data[0], "| Category:", data[1], "| Note:", data[2])
    except:
        print("No expenses found.\n")


def total_expense():
    total = 0
    try:
        with open("expenses.txt", "r") as f:
            for line in f:
                amount = int(line.split(",")[0])
                total += amount
        print("Total Expense:", total)
    except:
        print("No expenses found.\n")


while True:
    print("\n--- Expense Tracker ---")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Total Expense")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        add_expense()
    elif choice == "2":
        view_expenses()
    elif choice == "3":
        total_expense()
    elif choice == "4":
        print("Thank you!")
        break
    else:
        print("Invalid choice\n")

