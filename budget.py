# -----------------------------------------------
# P.5.5
# -----------------------------------------------
# • Create a "Budget" program which would:
#   • Let a user input their income.
#   • Let a user input their expenses.
#   • Show the user their Income Statement (the statement that shows the user's
#     income and expenditures, and also shows whether a user is making
#     profit or
#     loss for a given period).
#   • Show the user their Income and Expenditure Account (the detailed summary
#     of every income and expense, with their type and amount).
#   • Let the user exit the program.
#
# Recommendation on how it could be done:
#   • The program could have a class Entry with attributes money_type (income
#     or expenses) and amount. It could also have a str() method which would
#     return how the object should be printed.
#   • The program could have a class Budget with the attribute log and the
#     following methods:
#     1. init() - it would initialize a log attribute (empty at the beginning)
#        in which the created income and expenses objects could be placed.
#     2. add_income_entry(self, amount) - it would get the amount as an input,
#        create an income object and put it in a budget log.
#     3. add_expenses_entry(self, amount) - it would get the amount as an
#        input, create an expenses object and put it in a budget log.
#     4. print_income_statement(self) - to print the Income Statement.
#     5. print_ie_account(self) - to print the Income and Expenditure Account.
# -----------------------------------------------

total_income = []
total_expenses = []


def get_income():
    while True:
        try:
            income = abs(round(float(input("Enter your income > ")), 2))
            total_income.append(income)
            break
        except ValueError:
            print("Error: invalid value for income!")


def get_expenses():
    while True:
        try:
            expenses = abs(round(float(input("Enter your expenses > ")), 2))
            total_expenses.append(expenses)
            break
        except ValueError:
            print("Error: invalid value for expenses!")


def print_balance():
    print(40 * "=")
    print(f"Jusu balansas: {sum(total_income) - sum(total_expenses)}")
    print(40 * "=")


def print_report():
    print(40 * "=")
    print(f"Visos jusu ivestos pajamos: {total_income}")
    print(f"Visos jusu ivestos islaidos: {total_expenses}")
    print(40 * "=")


def main():
    while True:
        try:
            user_input = int(input("Įveskite norimą veiksmą:\n"
                                   "1 - įvesti pajamas\n"
                                   "2 - įvesti išlaidas\n"
                                   "3 - gauti balansą\n"
                                   "4 - parodyti ataskaitą\n"
                                   "5 - išeiti iš programos\n"
                                   "> "))
            if user_input == 1:
                get_income()
            elif user_input == 2:
                get_expenses()
            elif user_input == 3:
                print_balance()
            elif user_input == 4:
                print_report()
            elif user_input == 5:
                print("Goodbye!")
                break
            else:
                print(40 * "<")
                print("Error: Your action should be a number between 1 and 5!")
                print(40 * ">")
        except ValueError:
            print(40 * "<")
            print("Error: Invalid action!")
            print(40 * ">")


main()
