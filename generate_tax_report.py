from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

import excel_writer as ex
import transactions as t
from fifo_calc import calc_profit_fifo

# imported transactions file name
TRANSACTIONS_FILE_NAME = "LTC_transactions.xlsx"
TAX_REPORT_FILE_PATH = "LTC_tax_report.xlsx"

t.import_transactions_from_file(TRANSACTIONS_FILE_NAME, "Sells", t.sells)
t.import_transactions_from_file(TRANSACTIONS_FILE_NAME, "Buys", t.buys)

# print all imported transactions
print("Imported Transactions:")
t.print_transactions(t.buys, "buys")
t.print_transactions(t.sells, "sells")

# print header of table
table_format = "{:<50} {:<12} {:<12} {:<12} {:<12}"
print(table_format.format("Sell Transaction", "Buy Value", "Sell Value", "Profits", "Taxable"))

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

    print(table_format.format(str(sell_transaction),
                              round(buy_value, 2),
                              round(sell_value, 2),
                              round(sell_profit, 2),
                              round(taxable_profit, 2)))
    ex.add_row(sheet, row_num, False, "right", str(sell_transaction),
               round(buy_value, 2),
               round(sell_value, 2),
               round(sell_profit, 2),
               round(taxable_profit, 2))
    row_num += 1

    # add calculated values to sums
    sum_buy_value += round(buy_value, 2)
    sum_sell_value += round(sell_value, 2)
    sum_profits += round(sell_profit, 2)
    sum_taxable += round(taxable_profit, 2)

print()
# add sums to bottom of sheet
ex.add_row(sheet, row_num + 1, True, "right",
           "",
           str(round(sum_buy_value)),
           str(round(sum_sell_value, 2)),
           str(round(sum_profits, 2)),
           str(round(sum_taxable, 2)))

print("Auto-sizing columns to fit content")
ex.autosize_columns(sheet)
print(f"Write Workbook back to file {TAX_REPORT_FILE_PATH}")
workbook.save(TAX_REPORT_FILE_PATH)
print("\nTotal Profits: EUR {}, taxable: EUR {}".format(sum_profits, sum_taxable))
