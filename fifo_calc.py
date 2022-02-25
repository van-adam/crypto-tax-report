import datetime

import transactions as t


def calc_profit_fifo(sell: tuple) -> tuple:
    sell_date, total_sell_quantity, sell_price = sell
    # print("Sell Quantity: {}, Sell Turnover: {}".format(total_sell_quantity, sell_price))

    sell_outs = []
    quantity = 0.0
    while quantity != total_sell_quantity:
        try:
            buy = t.buys[0]
        except IndexError:
            print("Not enough crypto assets for the sale {}: list index out of range!".format(sell))
            latest_sell_out = sell_outs.pop()
            t.buys.insert(len(t.buys), latest_sell_out)
            print("Re-added latest sell out {} to buy transactions".format(latest_sell_out))
            return 0.0, 0.0, 0.0, 0.0

        buy_date, buy_quantity, buy_price = buy
        if (quantity + buy_quantity) == total_sell_quantity:
            # print("enough")
            quantity += buy_quantity

            taxable = is_taxable(buy_date, sell_date)

            t.buys.pop(0)
            sell_outs.append((buy_quantity, buy_price, taxable))
            # t.print_transactions(sell_outs, "sell_outs")
            break
        elif (quantity + buy_quantity) < total_sell_quantity:
            # print("too little")
            quantity += buy_quantity

            taxable = is_taxable(buy_date, sell_date)

            t.buys.pop(0)
            sell_outs.append((buy_quantity, buy_price, taxable))
            # t.print_transactions(sell_outs, "sell_outs")
        elif (quantity + buy_quantity) > total_sell_quantity:
            # print("too much")
            need = total_sell_quantity - quantity
            if need == 0.0:
                # print("BREAK")
                break

            quantity += need
            taxable = is_taxable(buy_date, sell_date)
            sell_out = (need, buy_price * need / buy_quantity, taxable)
            sell_outs.append(sell_out)
            # t.print_transactions(sell_outs, "sell_outs")

            # change transaction and re-add it to buy transactions
            rest = buy_quantity - need
            updated_buy = (buy_date, rest, buy_price * rest / buy_quantity)
            t.buys.pop(0)
            t.buys.insert(0, updated_buy)

    # calculate weighted buy price
    weighted_buy_price = 0.0
    total_profit = 0.0
    taxable_profit = 0.0
    for sell_out in sell_outs:
        buy_quantity, buy_price, taxable = sell_out

        share = (buy_quantity / total_sell_quantity)
        weighted_buy_price += buy_price * share

        weighted_profit = (sell_price - buy_price) * share
        total_profit += weighted_profit
        if taxable:
            taxable_profit += weighted_profit

    return weighted_buy_price, sell_price, round(total_profit, 2), round(taxable_profit, 2)


def is_taxable(buy_date: datetime.date, sell_date: datetime.date) -> bool:
    diff: datetime.timedelta = sell_date - buy_date
    if diff.days < 360:
        taxable = True
    else:
        taxable = False

    return taxable
