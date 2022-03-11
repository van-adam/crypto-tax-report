import logging


def take_all(quantity, buy_quantity, buy_price, sell_outs, taxable):
    quantity += buy_quantity
    sell_outs.append((buy_quantity, buy_price, taxable))
    log.debug("too little")
    print_sell_outs(sell_outs, "sell_outs")
    return quantity


def take_less(total_sell_quantity, quantity, buy_date, buy_quantity, buy_price, sell_outs, taxable):
    need = total_sell_quantity - quantity
    if need == 0.0:
        log.debug("BREAK")
        # break
    quantity += need
    sell_out = (need, buy_price * need / buy_quantity, taxable)
    sell_outs.append(sell_out)
    log.debug("too much")
    print_sell_outs(sell_outs, "sell_outs")
    # change transaction and re-add it to buy transactions
    rest = buy_quantity - need
    updated_buy = (buy_date, rest, buy_price * rest / buy_quantity)
    return quantity, updated_buy


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
