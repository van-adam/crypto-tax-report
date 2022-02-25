import transactions as t
from fifo_calc import calc_profit_fifo

# print all imported transactions
t.print_transactions(t.buys, "buys")
t.print_transactions(t.sells, "sells")

# print header of table
table_format = "{:<22} {:<12} {:<12} {:<12}"
print(table_format.format("Transaction", "Buy Price", "Sell Price", "Profits"))

# calculate total profits
total_profits = 0.0
for sell_transaction in t.sells:
    buy_value, sell_value, sell_profit = calc_profit_fifo(sell_transaction)

    print(table_format.format(str(sell_transaction),
                              round(buy_value, 2),
                              round(sell_value, 2),
                              round(sell_profit, 2)))
    total_profits += sell_profit

print("\nTotal Profits: EUR {}".format(total_profits))
