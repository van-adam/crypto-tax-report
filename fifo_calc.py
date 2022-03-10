import datetime
import logging

import config as c
import transactions as t


def calc_profit_fifo(sell: tuple) -> tuple:
    """
    Calculates the weighted buy price, sell price, total profit, and taxable profit from a sell transaction tuple.

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
            buy = t.buys[0]
        except IndexError:
            log.error("Not enough crypto assets for the sale {}: list index out of range!".format(sell))
            latest_sell_out = sell_outs.pop()
            t.buys.insert(len(t.buys), latest_sell_out)
            log.warning("Re-added latest sell out {} to buy transactions".format(latest_sell_out))
            return 0.0, 0.0, 0.0, 0.0

        buy_date, buy_quantity, buy_price = buy

        # round buy_quantity to 10 decimal places to avoid IndexError above
        buy_quantity = round(buy_quantity, 10)
        if (quantity + buy_quantity) == total_sell_quantity:
            quantity += buy_quantity

            taxable = is_taxable(buy_date, sell_date)

            t.buys.pop(0)
            sell_outs.append((buy_quantity, buy_price, taxable))
            log.debug("enough")
            print_sell_outs(sell_outs, "sell_outs")
            break
        elif (quantity + buy_quantity) < total_sell_quantity:
            quantity += buy_quantity

            taxable = is_taxable(buy_date, sell_date)

            t.buys.pop(0)
            sell_outs.append((buy_quantity, buy_price, taxable))
            log.debug("too little")
            print_sell_outs(sell_outs, "sell_outs")
        elif (quantity + buy_quantity) > total_sell_quantity:
            need = total_sell_quantity - quantity
            if need == 0.0:
                log.debug("BREAK")
                break

            quantity += need
            taxable = is_taxable(buy_date, sell_date)
            sell_out = (need, buy_price * need / buy_quantity, taxable)
            sell_outs.append(sell_out)
            log.debug("too much")
            print_sell_outs(sell_outs, "sell_outs")

            # change transaction and re-add it to buy transactions
            rest = buy_quantity - need
            updated_buy = (buy_date, rest, buy_price * rest / buy_quantity)
            t.buys.pop(0)
            t.buys.insert(0, updated_buy)

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


def is_taxable(buy_date: datetime.date, sell_date: datetime.date) -> bool:
    """
    Determines whether a sell transaction is taxable based on the buy date and sell date. A sale is taxable whenever
    the difference between buy date and sell date is smaller than 360 days.

    :param buy_date: the buy date
    :param sell_date: the sell date
    :return: true if the sale is taxable
    """
    diff: datetime.timedelta = sell_date - buy_date
    if diff.days < c.TAXFREE_TIMEDELTA:
        taxable = True
    else:
        taxable = False

    return taxable


def print_sell_outs(transactions: list, label: str) -> None:
    """
    Prints the passed list of transactions to the console.

    :param transactions: the transactions list
    :param label: the label above the output
    :return:
    """
    log.debug("{}{}".format(label, "*" * (50 - len(label))))

    for transaction in transactions:
        log.debug(to_string(transaction))

    log.debug("=" * 50)


def to_string(transaction: tuple) -> str:
    """
    Formats a transaction tuple as a String.

    :param transaction: the transaction tuple
    :return: a formatted String based on the tuple
    """
    quantity = transaction[0]
    price = transaction[1]

    if transaction[2]:
        taxable = "True"
    else:
        taxable = "False"

    return "{:<10} :: {:<10} :: {:<5}".format(quantity, price, taxable)


log = logging.getLogger()
