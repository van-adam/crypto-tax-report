import logging

from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from van.adam import transactions as t

import config as c
import excel_writer as x
import inventory_methods.fifo as fifo


def generate_tax_report(token_abbr: str) -> None:
    """
    Generates a tax report of the passed crypto token containing Sell Transaction, Token, Buy Value, Sell Value,
    Profits, and Taxable Profit. The report is created based on the [token_abbr]_transactions.xlsx of the passed token.

    :param token_abbr: the token abbreviation, e.g. LTC
    """
    transactions_file_path = c.TRANSACTIONS_DIR + token_abbr + "_transactions.xlsx"
    tax_report_file_path = c.TAX_REPORTS_DIR + token_abbr + "_tax_report.xlsx"

    t.import_transactions_from_file(transactions_file_path, "Sells", t.sells)
    t.import_transactions_from_file(transactions_file_path, "Buys", t.buys)

    # log all imported transactions
    log.info("Imported Transactions:")
    t.print_buys()
    t.print_sells()

    # log header of table
    tr_format = "{:<35} {:<5} {:<12} {:<12} {:<12} {:<12}"
    log.info(tr_format.format("Sell Transaction", "Token", "Buy Value", "Sell Value", "Profits", "Taxable"))

    # create workbook
    workbook: Workbook = Workbook()
    sheet: Worksheet = workbook.active
    row_num = 1

    # create sheet header
    x.add_row(sheet, 1, True, "left", "Sell Transaction", "Token", "Buy Value", "Sell Value", "Profits", "Taxable Profit")
    row_num += 1

    # calculate sums
    sum_buy_value = 0.0
    sum_sell_value = 0.0
    sum_profits = 0.0
    sum_taxable = 0.0
    for sell_transaction in t.sells:
        # get profits per sell transaction
        if c.USE_FIFO:
            buy_value, sell_value, sell_profit, taxable_profit = fifo.calc_profit(sell_transaction)
        else:
            buy_value, sell_value, sell_profit, taxable_profit = (0.0, 0.0, 0.0, 0.0)

        log.info(tr_format.format(t.to_string(sell_transaction), token_abbr,
                                  buy_value, sell_value, sell_profit, taxable_profit))
        x.add_row(sheet, row_num, False, "right", t.to_string(sell_transaction), token_abbr,
                  buy_value, sell_value, sell_profit, taxable_profit)
        row_num += 1

        # add calculated values to sums
        sum_buy_value += buy_value
        sum_sell_value += sell_value
        sum_profits += sell_profit
        sum_taxable += taxable_profit

    log.info("Total Profits: {}, taxable: {}".format(round(sum_profits, 2), round(sum_taxable, 2)))
    # add sums to bottom of sheet
    x.add_row(sheet, row_num + 1, True, "right",
              "",
              "",
              round(sum_buy_value, 2),
              round(sum_sell_value, 2),
              round(sum_profits, 2),
              round(sum_taxable, 2))

    log.info("Auto-sizing columns to fit content")
    x.autosize_columns(sheet)
    log.info(f"Write Workbook to file {tax_report_file_path}")
    workbook.save(tax_report_file_path)


logging.basicConfig(level=c.LOG_LEVEL, format="%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
log = logging.getLogger()

for token in c.tokens:
    generate_tax_report(token)
