from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet


# tuple: (date: datetime.date, quantity: float, price: float); sorted by date ascending
sells = []
buys = []

# sells = [
#     (d.date(2021, 4, 16), 0.13541820, 35),     # 29.58
#     (d.date(2021, 4, 21), 0.11454640, 25),     # 22.68
#     (d.date(2021, 4, 22), 0.13420283, 30),     # 25.89
#     (d.date(2021, 5, 3), 0.36125077, 88.09),  # 80.48
# ]                                 # Total Profits: EUR 158.63
#
# buys = [
#     (d.date(2020, 5, 27), 0.18586880, 7.44),
#     (d.date(2020, 5, 27), 0.08721041, 3.49),
#     (d.date(2020, 6, 4), 0.27289865, 11.71),
#     (d.date(2020, 6, 10), 0.27456618, 11.22),
# ]


# sells = [
#     (d.date(2021, 5, 1), 3.0, 100),
#     (d.date(2021, 6, 1), 1.0, 50),
#     (d.date(2021, 7, 1), 2.0, 120),
#     (d.date(2021, 8, 1), 2.0, 150),
# ]
#
# buys = [
#     (d.date(2020, 5, 1), 1.0, 10),
#     (d.date(2020, 6, 1), 2.0, 25),
#     (d.date(2020, 7, 1), 2.0, 45),
#     (d.date(2020, 8, 1), 3.0, 60),
# ]

# Profit: 80
# Profit: 27.5
# Profit: 98.75
# Profit: 110


def import_transactions_from_file(file_path: str, sheet_name: str, destination_list: list) -> None:
    workbook = load_workbook(file_path)
    sheet: Worksheet = workbook[sheet_name]

    if len(destination_list) == 0:
        for row in range(2, sheet.max_row + 1):
            date = sheet.cell(row, 1).value
            date = date.date()
            quantity = sheet.cell(row, 2).value
            price = sheet.cell(row, 3).value

            destination_list.append((date, quantity, price))

        print("Imported transactions from file '{}' from sheet '{}'".format(file_path, sheet_name))


def print_buys():
    print_transactions(buys, "BUYS")


def print_sells():
    print_transactions(sells, "SELLS")


def print_transactions(transactions: list, label: str) -> None:
    print(label, "*" * (50 - len(label)))

    for item in transactions:
        print(item)

    print("=" * 50)
