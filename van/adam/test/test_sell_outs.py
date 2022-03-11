import logging
from unittest import TestCase
import datetime as d

from van.adam.inventory_methods.sell_outs import take_all, take_less, to_string


class Test(TestCase):
    logging.basicConfig(level="DEBUG", format="%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")

    def test_take_all(self):
        quantity = 2.0
        sell_outs = [
            (1.0, 50.0, True),
        ]
        buy_quantity, buy_price = (3.0, 100.0)
        taxable = True

        quantity = take_all(quantity, buy_quantity, buy_price, sell_outs, taxable)
        self.assertEqual(5.0, quantity)
        self.assertEqual(2, len(sell_outs))
        self.assertEqual((3.0, 100.0, True), sell_outs[1])

    def test_take_less(self):
        total_sell_quantity = 3.0
        quantity = 2.0
        buy_date, buy_quantity, buy_price = (d.date(2021, 3, 14), 5.0, 200.0)
        sell_outs = [
            (1.0, 50.0, True),
        ]
        taxable = True

        quantity, updated_buy = take_less(total_sell_quantity, quantity, buy_date, buy_quantity, buy_price, sell_outs, taxable)
        self.assertEqual(3.0, quantity)
        self.assertEqual(2, len(sell_outs))
        self.assertEqual((1.0, buy_price * 1.0 / buy_quantity, True), sell_outs[1])
        self.assertEqual((buy_date, 4.0, buy_price * 4.0 / buy_quantity), updated_buy)


    def test_to_string(self):
        output = to_string((1.0, 50, True))
        self.assertEqual("1.0        :: 50         :: True ", output)