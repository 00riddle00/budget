# -----------------------------------------------
# P.6.3
# -----------------------------------------------
# • Patobulinti 5 pamokos biudžeto programą taip, kad joje:
#
#   • Irasas klasėje būtų tik vienas atributas suma, ir būtų sukurtos dvi
#     vaikinės klasės PajamuIrasas ir IslaiduIrasas.
#   • Klasė PajamuIrasas turėtų du papildomus atributus siuntejas ir
#     papildoma_informacija.
#   • Klasė IslaiduIrasas turėtų du papildomus atributus atsiskaitymo_budas ir
#     isigyta_preke_paslauga.
#   • Klasės Biudzetas metodai parodyti_balansa() ir parodyti_ataskaita() būtų
#     perdaryti taip, kad jie nuskaitytų kiekvieną įrašą iš žurnalo ir
#     atpažinę, ar tai pajamų įrašas, ar išlaidų (pvz., naudojant Python
#     funkciją isinstance()), atspausdintų reikiamą informaciją kaip ir prieš
#     tai.
#   • Būtų vartotojo sąsaja per komandinę eilutę (Command-Line Interface (CLI),
#     kas savo ruožtu yra vienas iš galimų Text-Based User Interface (TUI)
#     tipų), per kurią vartotojas galėtų įvesti pajamų ir išlaidų įrašus po
#     vieną ir pamatyti balansą bei ataskaitą.
# -----------------------
# • Modify the "Budget" program from the previous lesson (Python lesson 5,
#   exercise no. 5) so that it would have:
#
#   • The Entry class only have a single attribute amount, and create its child
#     classes IncomeEntry and ExpensesEntry.
#   • The IncomeEntry class have two additional attributes sender and
#     additional_info.
#   • The ExpensesEntry class have two additional attributes payment_option and
#     received_good_or_service.
#   • Refactored Budget class methods print_income_statement() and
#     print_ie_account() so that they would read every entry in a log and
#     recognize whether it is an income entry or an expenses entry (for
#     example, using the isinstance() method) and print the required
#     information as previously.
#   • A Command-Line Interface (CLI) (one possible type of a Text-Based User
#     Interface (TUI)) so that a user, using the command-line, could enter the
#     income and expenses entries one by one, and view both the Income
#     Statement and Income and Expenditure Account.
# -----------------------------------------------


class Entry:
    def __init__(self, amount):
        self.amount = amount


class IncomeEntry(Entry):
    def __init__(self, amount, sender, info):
        super().__init__(amount)
        self.sender = sender
        self.info = info

    def __str__(self):
        return (
            f"Income: {self.amount}, Sender: {self.sender}, Additional info: {self.info}")


class ExpensesEntry(Entry):
    def __init__(self, amount, payment_option, received_good_or_service):
        super().__init__(amount)
        self.payment_option = payment_option
        self.received_good_or_service = received_good_or_service

    def __str__(self):
        return (
            f"Expenses: {self.amount}, Payment option: {self.payment_option}, "
            f"Received good or service: {self.received_good_or_service}")


class Budget:
    def __init__(self):
        self.log = []
        self.total_income = []
        self.total_expenses = []

    def add_income_entry(self, income, sender, info):
        entry = IncomeEntry(income, sender, info)
        self.total_income.append(income)
        self.log.append(entry)

    def add_expenses_entry(self, expenses, payment_option, received_good_or_service):
        entry = ExpensesEntry(expenses, payment_option, received_good_or_service)
        self.total_expenses.append(expenses)
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


def main():
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
                    income = abs(round(float(input("Enter your income: ")), 2))
                    sender = str(input("Enter the sender: "))
                    info = str(input("Enter more info about the transaction: "))
                    budget.add_income_entry(income, sender, info)
                case 2:
                    expenses = abs(round(float(input("Enter your expenses: ")), 2))
                    payment_option = str(input("Enter the payment option: "))
                    received_good_or_service = str(input("Enter more info about the receiced good or service: "))
                    budget.add_expenses_entry(expenses, payment_option, received_good_or_service)
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


if __name__ == "__main__":
    main()
