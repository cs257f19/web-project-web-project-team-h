import unittest
from datasource import *

class DataSourceTester(unittest.TestCase):
    def setUp(self):
        self.ds = DataSource()

    def test_integer(self):
        listingId = 12
        self.assertTrue(self.ds.getL(listingId))

    def test_not_integer(self):
        listingId = 12
        self.assertFalse(self.ds.integer(listingId))

    def test_num_digits_bigger_3(self):
        num = 4
        self.assertTrue(self.ds.num(num))

    def test_num_digits_not_bigger_3(self):
        num = 2
        self.assertFalse(self.ds.integer(num))


if __name__ == '__main__':
    unittest.main()