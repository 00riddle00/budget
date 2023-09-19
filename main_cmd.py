# -----------------------------------------------
# P.7.6
# -----------------------------------------------
# • Perdaryti biudžeto programą su klasėmis (iš praėjusios paskaitos) taip,
#   kad:
#   • Kiekviena klasė persikeltų į atskirą, tik jai skirtą .py failą.
#   • Pajamos ir išlaidos programos pradžioje būtų nuskaitytos (angl. loaded)
#     iš .pkl failo (naudojant modulį pickle).
#   • Pajamos ir išlaidos programos pabaigoje būtų išsaugotos (angl. dumped) į
#     .pkl failą (naudojant modulį pickle).
#
# Galima pasirinkti, kaip pajamos ir išlaidos bus išsaugomos į .pkl failą –
# kaip objektas, kaip skaičių sąrašas, ar pan. – svarbu, kad iš .pkl failo būtų
# nuskaitoma tokiu pat būdu (į objektą, į skaičių sąrašą, ar pan.).
# -----------------------
# • Refactor the "Budget" program from the previous lesson (Python lesson 6,
#   exercise no. 3) such that:
#   • Every class appears in its own .py file.
#   • Income and expenses are loaded from a .pkl file at the start of the
#     program (using pickle module).
#   • Income and expenses are saved (dumped) to a .pkl file at the end of the
#     program (using pickle module).
#
# You can chooose how income and expenses are saved to a .pkl file - as an
# object, as a list of numbers, etc. - the important thing is that they should
# be loaded in the same way (into an object, a list of numbers, etc.).
# -----------------------------------------------

from budget import Budget

budget = Budget()


def main():
    while True:
        try:
            choice = int(input("Enter the desired action:\n"
                               "1 - Add income.\n"
                               "2 - Add expenses.\n"
                               "3 - View income statement (balance).\n"
                               "4 - View income and expenditure account (report).\n"
                               "5 - Save your budget to a file.\n"
                               "6 - Read your budget from a file.\n"
                               "7 - Quit.\n"
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
                    budget.save_to_file()
                    print("Your entries have been saved to the budget list.")
                case 6:
                    print("Here is your budget list:")
                    budget.extract_from_file()
                    budget.print_ie_account()
                case 7:
                    print("Goodbye!")
                    break
                case _:
                    print("Error: Your action should be a number between 1 and 7!")
        except ValueError:
            print("Error: Invalid action or value!")


if __name__ == "__main__":
    main()
