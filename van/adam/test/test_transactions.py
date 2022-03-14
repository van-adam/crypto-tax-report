import logging
from van.adam import transactions as t
import datetime as d

from unittest import TestCase

file_path = "../transactions/transactions_example.xlsx"


class Test(TestCase):
    logging.basicConfig(level="DEBUG",
                        format="%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")

    def test_import_transactions_from_file(self):
        sells = []
        buys = []
        t.import_transactions_from_file(file_path, "Sells", sells)
        t.import_transactions_from_file(file_path, "Buys", buys)

        self.assertEqual(4, len(sells))
        self.assertEqual(4, len(buys))

        for sell in sells:
            self.assertIsNotNone(sell)
        for buy in buys:
            self.assertIsNotNone(buy)

        self.assertEqual(35.0, sells[0][2])
        self.assertEqual(30.0, sells[2][2])

        self.assertEqual(3.49, buys[1][2])
        self.assertEqual(11.22, buys[3][2])

    def test_import_transactions_from_file_non_empty_list(self):
        non_empty_list = [(d.date(2022, 3, 10), 1.0, 5.0)]
        self.assertEqual(1, len(non_empty_list), "should be 1")

        t.import_transactions_from_file(file_path, "Sells", non_empty_list)
        self.assertEqual(4, len(non_empty_list), "should be 4")

    def test_to_string(self):
        transaction = (d.date(2021, 4, 16), 0.1354182, 35.0)
        output = t.to_string(transaction)
        self.assertEqual("16-04-2021: 0.1354182  :: 35.00  ", output)

    def test_is_taxable(self):
        sells = []
        buys = []
        t.import_transactions_from_file(file_path, "Sells", sells)
        t.import_transactions_from_file(file_path, "Buys", buys)
        # over 1 year
        sell_date = sells[0][0]
        buy_date = buys[0][0]
        self.assertTrue(t.is_taxable(buy_date, sell_date))

        # under 1 year
        sell_date = sells[3][0]
        buy_date = buys[0][0]
        self.assertFalse(t.is_taxable(buy_date, sell_date))