from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

import excel_writer as ex
import transactions as t
from fifo_calc import calc_profit_fifo


# constants
TRANSACTIONS_FILE_NAME = "LTC_transactions.xlsx"
TAX_REPORT_FILE_PATH = "LTC_tax_report.xlsx"

t.import_transactions_from_file(TRANSACTIONS_FILE_NAME, "Sells", t.sells)
t.import_transactions_from_file(TRANSACTIONS_FILE_NAME, "Buys", t.buys)

# print all imported transactions
print("Imported Transactions:")
t.print_transactions(t.buys, "buys")
t.print_transactions(t.sells, "sells")

# print header of table
tr_format = "{:<35} {:<12} {:<12} {:<12} {:<12}"
print(tr_format.format("Sell Transaction", "Buy Value", "Sell Value", "Profits", "Taxable"))

# create workbook
workbook: Workbook = Workbook()
sheet: Worksheet = workbook.active
row_num = 1

# create sheet header
ex.add_row(sheet, 1, True, "left", "Sell Transaction", "Buy Value", "Sell Value", "Profits", "Taxable Profit")
row_num += 1

# calculate sums
sum_buy_value = 0.0
sum_sell_value = 0.0
sum_profits = 0.0
sum_taxable = 0.0
for sell_transaction in t.sells:
    # get profits per sell transaction
    buy_value, sell_value, sell_profit, taxable_profit = calc_profit_fifo(sell_transaction)

    print(tr_format.format(t.to_string(sell_transaction), buy_value, sell_value, sell_profit, taxable_profit))
    ex.add_row(sheet, row_num, False, "right", t.to_string(sell_transaction), buy_value, sell_value, sell_profit, taxable_profit)
    row_num += 1

    # add calculated values to sums
    sum_buy_value += buy_value
    sum_sell_value += sell_value
    sum_profits += sell_profit
    sum_taxable += taxable_profit

print("\nTotal Profits: EUR {}, taxable: EUR {}".format(sum_profits, sum_taxable))
# add sums to bottom of sheet
ex.add_row(sheet, row_num + 1, True, "right",
           "",
           round(sum_buy_value, 2),
           round(sum_sell_value, 2),
           round(sum_profits, 2),
           round(sum_taxable, 2))

print("\nAuto-sizing columns to fit content")
ex.autosize_columns(sheet)
print(f"Write Workbook to file {TAX_REPORT_FILE_PATH}")
workbook.save(TAX_REPORT_FILE_PATH)
