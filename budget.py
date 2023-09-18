# -----------------------------------------------
# P.5.5
# -----------------------------------------------
# • Padaryti biudžeto programą, kuri:
#   • Leistų vartotojui įvesti pajamas.
#   • Leistų vartotojui įvesti išlaidas.
#   • Leistų vartotojui parodyti pajamų/išlaidų balansą.
#   • Leistų vartotojui parodyti biudžeto ataskaitą (visus pajamų ir išlaidų
#     įrašus su sumomis).
#   • Leistų vartotojui išeiti iš programos.
#
# Rekomendacija, kaip galima būtų padaryti:
#   • Programa turi turėti klasę Irasas, kuri turėtų argumentus tipas (Pajamos
#     arba Išlaidos) ir suma. Galima prirašyti str() metodą, kuris grąžintų,
#     kaip bus atvaizduojamas spausdinamas objektas.
#   • Programa turi turėti klasę Biudzetas, kurioje būtų:
#     1. Metodas init(), kuriame sukurtas tuščias sąrašas zurnalas, į kurį bus
#        dedami sukurti pajamų ir išlaidų objektai.
#     2. Metodas prideti_pajamu_irasa(self, suma), kuris priimtų paduotą sumą,
#        sukurtų pajamų objektą ir įdėtų jį į biudžeto žurnalą.
#     3. Metodas prideti_islaidu_irasa(self, suma), kuris priimtų paduotą sumą,
#        sukurtų išlaidų objektą ir įdėtų jį į biudžeto žurnalą.
#     4. Metodas gauti_balansą(self), kuris grąžintų žurnale laikomų pajamų ir
#        išlaidų balansą.
#     5. Metodas parodyti_ataskaita(self), kuris atspausdintų visus pajamų ir
#        išlaidų įrašus (nurodydamas kiekvieno įrašo tipą ir sumą).
# -----------------------
# • Create a "Budget" program which would:
#   • Let a user input their income.
#   • Let a user input their expenses.
#   • Show the user their Income Statement (the statement that shows the user's
#     income and expenditures, and also shows whether a user is making
#     profit or loss for a given period).
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

class Entry:
    def __init__(self, money_type, amount):
        self.money_type = money_type
        self.amount = amount

    def __str__(self):
        return f"[{self.money_type}]: {self.amount} €"


class Budget:
    def __init__(self):
        self.log = []
        self.total_income = []
        self.total_expenses = []

    def add_income_entry(self, amount):
        entry = Entry("Income", amount)
        self.total_income.append(amount)
        self.log.append(entry)

    def add_expenses_entry(self, amount):
        entry = Entry("Expenses", amount)
        self.total_expenses.append(amount)
        self.log.append(entry)

    # a.k.a. balance
    def print_income_statement(self):
        print(40 * "-")
        profit_loss = sum(self.total_income) - sum(self.total_expenses)

        print("Income statement:")
        print(f"Total income: {sum(self.total_income)} €")
        print(f"Total expenses: {sum(self.total_expenses)} €")
        print(f"Your balance: {profit_loss} €")

        if profit_loss > 0:
            print("You are making a profit!")
        elif profit_loss < 0:
            print("You are making a loss.")
        print(40 * "-")

    # a.k.a. report
    def print_ie_account(self):
        print(40 * "-")
        print("Income and Expenditure Account:")
        for entry in self.log:
            print(entry)
        print(40 * "-")


budget = Budget()

while True:
    try:
        choice = int(input("Enter the desired action:\n"
                           "1 - Add income.\n"
                           "2 - Add expenses.\n"
                           "3 - View income statement (balance).\n"
                           "4 - View income and expenditure account (report).\n"
                           "5 - Quit.\n"
                           "> "))

        match choice:
            case 1:
                income_amount = abs(round(float(input("Enter your income: ")), 2))
                budget.add_income_entry(income_amount)
            case 2:
                expenses_amount = abs(round(float(input("Enter your expenses: ")), 2))
                budget.add_expenses_entry(expenses_amount)
            case 3:
                budget.print_income_statement()
            case 4:
                budget.print_ie_account()
            case 5:
                print("Goodbye!")
                break
            case _:
                print("Error: Your action should be a number between 1 and 5!")
    except ValueError:
        print("Error: Invalid action or value!")
