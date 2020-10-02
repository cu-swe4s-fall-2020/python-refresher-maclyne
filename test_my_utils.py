"""Testing library of functions in my_utils.py

    Initial date: 1 Oct 2020
    Author: Margot Clyne

"""
import unittest
import my_utils
import array

class TestCalc(unittest.TestCase):
    def test_get_column(self):
        self.assertEqual(my_utils.get_column('covid-19-data/us-counties-testfile-Boulder.csv', 0, '2020-09-04', result_column=4),array.array('i',[2399]))

if __name__ == '__main__':
    unittest.main()

