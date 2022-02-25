import transactions as t


def calc_profit_fifo(sell: tuple) -> tuple:
    sell_quantity, sell_price = sell
    # print("Sell Quantity: {}, Sell Turnover: {}".format(sell_quantity, sell_price))

    sell_outs = []
    quantity = 0.0
    while quantity != sell_quantity:
        try:
            buy = t.buys[0]
        except IndexError:
            print("Not enough crypto assets for the sale {}: list index out of range!".format(sell))
            latest_sell_out = sell_outs.pop()
            t.buys.insert(len(t.buys), latest_sell_out)
            print("Re-added latest sell out {} to buy transactions".format(latest_sell_out))
            return 0.0, 0.0, 0.0

        buy_quantity = buy[0]
        if (quantity + buy_quantity) == sell_quantity:
            # print("enough")
            quantity += buy_quantity
            sell_outs.append(t.buys.pop(0))
            # t.print_transactions(sell_outs, "sell_outs")
            break
        elif (quantity + buy_quantity) < sell_quantity:
            # print("too little")
            quantity += buy_quantity
            sell_outs.append(t.buys.pop(0))
            # t.print_transactions(sell_outs, "sell_outs")
        elif (quantity + buy_quantity) > sell_quantity:
            # print("too much")
            need = sell_quantity - quantity
            if need == 0.0:
                # print("BREAK")
                break

            quantity += need
            sell_out = (need, buy[1] * need / buy_quantity)
            sell_outs.append(sell_out)
            # t.print_transactions(sell_outs, "sell_outs")

            # change transaction and re-add it to buy transactions
            rest = buy_quantity - need
            new_buy = (rest, buy[1] * rest / buy_quantity)
            t.buys.pop(0)
            t.buys.insert(0, new_buy)

    # calculate weighted buy price
    buy_price = 0.0
    for sell_out in sell_outs:
        sell_out_quantity = sell_out[0]
        sell_out_price = sell_out[1]
        buy_price += sell_out_price * (sell_out_quantity / sell_quantity)

    profit = sell_price - buy_price
    return buy_price, sell_price, round(profit, 2)