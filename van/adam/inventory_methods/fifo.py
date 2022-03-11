import logging

from van.adam import transactions as t
from van.adam.inventory_methods.output import calculate_output
from van.adam.inventory_methods.sell_outs import take_all, take_less
from van.adam.transactions import is_taxable


def calc_profit(sell: tuple) -> tuple:
    """
    Calculates the buy price, sell price, total profit, and taxable profit from a sell transaction tuple.

    :param sell: the sell transaction as a tuple (date: datetime.date, quantity: float, price: float)
    :return: a tuple containing (weighted_buy_price: float, sell_price: float, total_profit: float, taxable_profit:
    float); all numbers are rounded to two decimal places
    """
    sell_date, total_sell_quantity, sell_price = sell

    sell_outs = []
    quantity = 0.0
    while quantity != total_sell_quantity:
        log.debug("quantity: {}".format(quantity))
        try:
            buy = t.buys.pop(0)
        except IndexError:
            log.error("Not enough crypto assets for the sale {}: list index out of range!".format(sell))
            latest_sell_out = sell_outs.pop()
            t.buys.insert(len(t.buys), latest_sell_out)
            log.warning("Re-added latest sell out {} to buy transactions".format(latest_sell_out))
            return 0.0, 0.0, 0.0, 0.0

        buy_date, buy_quantity, buy_price = buy

        # round buy_quantity to 10 decimal places to avoid IndexError above
        buy_quantity = round(buy_quantity, 10)
        taxable = is_taxable(buy_date, sell_date)
        if (quantity + buy_quantity) == total_sell_quantity:
            quantity = take_all(quantity, buy_quantity, buy_price, sell_outs, taxable)
        elif (quantity + buy_quantity) < total_sell_quantity:
            quantity = take_all(quantity, buy_quantity, buy_price, sell_outs, taxable)
        elif (quantity + buy_quantity) > total_sell_quantity:
            quantity, updated_buy = take_less(total_sell_quantity, quantity, buy_date, buy_quantity, buy_price,
                                              sell_outs, taxable)
            t.buys.insert(0, updated_buy)

    return calculate_output(sell_outs, total_sell_quantity, sell_price)


log = logging.getLogger()
