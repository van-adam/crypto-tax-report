import logging


def take_all(quantity, buy_quantity, buy_price, sell_outs, taxable):
    """
    Takes the entire quantity of the buy transaction into the sell outs.

    :param quantity: the current quantity that was taken for the sell transaction
    :param buy_quantity: the token quantity of this buy transaction
    :param buy_price: how much the tokens of this buy transaction cost
    :param sell_outs: the sell outs (buy transactions taken for a sell transaction)
    :param taxable: whether the sell transaction is taxable
    :return: the current quantity that was taken for the sell transaction
    """
    quantity += buy_quantity
    sell_outs.append((buy_quantity, buy_price, taxable))
    log.debug("need all tokens of this buy transaction")
    print_sell_outs(sell_outs, "sell_outs")
    return quantity


def take_less(total_sell_quantity, quantity, buy_date, buy_quantity, buy_price, sell_outs, taxable):
    """
    Takes less than the quantity of the buy transaction into the sell outs and updates the buy transaction with the
    remaining quantity and buy price.

    :param total_sell_quantity: the quantity needed for the sell transaction
    :param quantity: the current quantity that was taken for the sell transaction
    :param buy_date: the date the buy transaction occurred
    :param buy_quantity: the token quantity of this buy transaction
    :param buy_price: how much the tokens of this buy transaction cost
    :param sell_outs: the sell outs (buy transactions taken for a sell transaction)
    :param taxable: whether the sell transaction is taxable
    :return: a tuple of the current quantity that was taken for the sell transaction and the updated buy transaction
    """
    need = total_sell_quantity - quantity
    if need == 0.0:
        log.debug("BREAK")
        return quantity, (None, 0.0, 0.0)
    quantity += need
    sell_out = (need, buy_price * need / buy_quantity, taxable)
    sell_outs.append(sell_out)
    log.debug("need less tokens than this buy transaction")
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
