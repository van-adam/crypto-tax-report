import logging
import fifo_calc as f
import transactions as t
import datetime as d

from unittest import TestCase


def test_init():
    t.sells = [
        (d.date(2021, 5, 1), 3.0, 100),
        (d.date(2021, 6, 1), 1.0, 50),
        (d.date(2021, 7, 1), 2.0, 120),
        (d.date(2021, 8, 1), 2.0, 150),
    ]

    t.buys = [
        (d.date(2020, 5, 1), 1.0, 10),
        (d.date(2020, 6, 1), 2.0, 25),
        (d.date(2020, 7, 1), 2.0, 45),
        (d.date(2020, 8, 1), 3.0, 60),
        (d.date(2020, 9, 1), 4.0, 100),
    ]

    # t.sells = [
    #     (d.date(2021, 4, 16), 0.13541820, 35),
    #     (d.date(2021, 4, 21), 0.11454640, 25),
    #     (d.date(2021, 4, 22), 0.13420283, 30),
    #     (d.date(2021, 5, 3), 0.36125077, 88.09),
    # ]
    #
    # t.buys = [
    #     (d.date(2020, 5, 27), 0.18586880, 7.44),
    #     (d.date(2020, 5, 27), 0.08721041, 3.49),
    #     (d.date(2020, 6, 4), 0.27289865, 11.71),
    #     (d.date(2020, 6, 10), 0.27456618, 11.22),
    # ]


class Test(TestCase):
    logging.basicConfig(level="DEBUG",
                        format="%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")

    def test_calc_profit_fifo(self):
        test_init()
        sell = t.sells[0]
        self.assertEqual((35, 100, 65, 41.67), f.calc_profit_fifo(sell))
        sell = t.sells[1]
        self.assertEqual((22.5, 50, 27.5, 27.5), f.calc_profit_fifo(sell))
        sell = t.sells[2]
        self.assertEqual((42.5, 120, 77.5, 40.0), f.calc_profit_fifo(sell))
        sell = t.sells[3]
        self.assertEqual((40, 150, 110, 0), f.calc_profit_fifo(sell))

        self.assertEqual((0.0, 0.0, 0.0, 0.0), f.calc_profit_fifo((d.date(2021, 9, 1), 15.0, 500)))

    def test_is_taxable(self):
        test_init()
        # over 1 year
        sell_date = t.sells[0][0]
        buy_date = t.buys[0][0]
        self.assertFalse(f.is_taxable(buy_date, sell_date))

        # under 1 year
        sell_date = t.sells[0][0]
        buy_date = t.buys[3][0]
        self.assertTrue(f.is_taxable(buy_date, sell_date))

    def test_to_string(self):
        output = f.to_string((1.0, 50, True))
        self.assertEqual("1.0        :: 50         :: True ", output)
