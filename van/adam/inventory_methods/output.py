def calculate_output(sell_outs, total_sell_quantity, sell_price):
    # calculate weighted buy price
    total_buy_price = 0.0
    total_profit = 0.0
    taxable_profit = 0.0
    for sell_out in sell_outs:
        buy_quantity, buy_price, taxable = sell_out

        total_buy_price += buy_price

        sell_share = (buy_quantity / total_sell_quantity)
        weighted_profit = sell_price * sell_share - buy_price
        total_profit += weighted_profit
        if taxable:
            taxable_profit += weighted_profit

    return round(total_buy_price, 2), round(sell_price, 2), round(total_profit, 2), round(taxable_profit, 2)