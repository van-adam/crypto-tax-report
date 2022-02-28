from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

import transactions as t
import excel_writer as ex
from fifo_calc import calc_profit_fifo

TAX_REPORT_FILE_PATH = "tax_report.xlsx"

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
ex.add_header_cell(sheet, "Sell Transaction", "Buy Value", "Sell Value", "Profits", "Taxable Profit")
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
    ex.add_row(sheet, row_num, str(sell_transaction),
               round(buy_value, 2),
               round(sell_value, 2),
               round(sell_profit, 2),
               round(taxable_profit, 2))
    row_num += 1

    sum_buy_value += buy_value
    sum_sell_value += sell_value
    sum_profits += sell_profit
    sum_taxable += taxable_profit

print()
# add sums to bottom of sheet
ex.add_row(sheet, row_num + 1, "",
           str(round(sum_buy_value)),
           str(round(sum_sell_value, 2)),
           str(round(sum_profits, 2)),
           str(round(sum_taxable, 2)))

print("Auto-sizing columns to fit content")
ex.autosize_columns(sheet)
print(f"Write Workbook back to file {TAX_REPORT_FILE_PATH}")
workbook.save(TAX_REPORT_FILE_PATH)
print("\nTotal Profits: EUR {}, taxable: EUR {}".format(sum_profits, sum_taxable))
