import unittest
from datasource import *

class DataSourceTester(unittest.TestCase):
    def setUp(self):
        self.ds = DataSource()

    def test_not_list(self):
        list_of_nums = 12
        self.assertEqual(self.ds.getAverage(list_of_nums),"Input not list")

    def test_invalid_list(self):
        list_of_nums = ['a',4,6]
        self.assertEqual(self.ds.getAverage(list_of_nums),"Invalid input")

    def test_response(self):
        list_of_nums = [8,4,6]
        self.assertEqual(self.ds.getAverage(list_of_nums),6.00)


if __name__ == '__main__':
    unittest.main()