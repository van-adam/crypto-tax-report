from van.adam import config as c
from unittest import TestCase


class MyTestCase(TestCase):
    def test_config(self):
        self.assertEqual("INFO", c.LOG_LEVEL)
        self.assertEqual("transactions/", c.TRANSACTIONS_DIR)
        self.assertEqual("tax_reports/", c.TAX_REPORTS_DIR)