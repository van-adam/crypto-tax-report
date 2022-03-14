import logging


def calculate_output(sell_outs, sell_quantity, sell_price):
    """
    Calculates the values for each row in the tax report based on the passed sell outs.

    :param sell_outs: the sell outs (buy transactions taken for a sell transaction)
    :param sell_quantity: the quantity needed for the sell transaction
    :param sell_price: how much was made with the sell transaction
    :return: tuple with total buy price, sell price, total profit, and taxable profit
    """
    # verify that sum of sell out quantities is equal to sell quantity
    sell_out_quantity = 0.0
    for sell_out in sell_outs:
        sell_out_quantity += sell_out[0]
    if sell_out_quantity != sell_quantity:
        log.error("Total Sell Out Quantity is not equal to Sell Quantity: {} : {}"
                  .format(sell_out_quantity, sell_quantity))

    # calculate weighted buy price
    total_buy_price = 0.0
    total_profit = 0.0
    taxable_profit = 0.0
    for sell_out in sell_outs:
        buy_quantity, buy_price, taxable = sell_out

        total_buy_price += buy_price

        sell_share = (buy_quantity / sell_quantity)
        weighted_profit = sell_price * sell_share - buy_price
        total_profit += weighted_profit
        if taxable:
            taxable_profit += weighted_profit

    return round(total_buy_price, 2), round(total_profit, 2), round(taxable_profit, 2)


log = logging.getLogger()
