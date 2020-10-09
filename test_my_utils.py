"""Testing library of functions in my_utils.py

    Initial date: 1 Oct 2020
    Author: Margot Clyne

"""
import unittest
import my_utils
import array
import random
import numpy as np
# Not sure if I am allowed to import numpy here, \
# but I need it for running_average, so...


class TestCalc(unittest.TestCase):
    def test_get_column(self):
        # check that this is the correct CSV file of covid data \
        # for comparing tests with (subset of last 20 days of Boulder county)
        self.assertEqual(my_utils.get_column(
                        'covid-19-data/us-counties-testfile-Boulder.csv',
                         0, '2020-09-04', result_column=4),
                         array.array('i', [2399]))
        # empty array of int if the query value is not in the file.
        self.assertEqual(my_utils.get_column(
                        'covid-19-data/us-counties-testfile-Boulder.csv',
                         1, 'Denver', result_column=4), array.array('i', []))
        # error mode raised if file not found
        self.assertRaises(FileNotFoundError, my_utils.get_column(
                         'name-of-some-file-that-doesnt-exist-in-path.csv',
                          0, '2020-09-04', result_column=4))

    def test_get_daily_count(self):
        # if only one day of cases input, daily count is that single number
        self.assertEqual(my_utils.get_daily_count(array.array('i', [3])),
                         array.array('i', [3]))
        # basic case of one new case each day
        self.assertTrue(all(my_utils.get_daily_count(array.array('i',
                                                                 [0, 1, 2, 3]))
                            == array.array('i', [0, 1, 1, 1])))
        # not increasing, but not decreasing
        self.assertTrue(all(my_utils.get_daily_count(array.array('i',
                                                                 [0, 2, 2]))
                            == array.array('i', [0, 2, 0])))
        # include randomness in tests
        r1 = random.randint(0, 100)
        r2 = random.randint(0, 100)
        r3 = random.randint(0, 100)
        r4 = random.randint(0, 100)
        cumul_in = array.array('i', [r1, r1+r2, r1+r2+r3, r1+r2+r3+r4])
        daily_out = array.array('i', [r1, r2, r3, r4])
        self.assertTrue(all(my_utils.get_daily_count(cumul_in) == daily_out))

        # TODO: test error modes (if any)
        # I am confused because I put an if statement for not decreasing \
        # and then exiting with code 2, but not sure how this all fits together
        self.assertTrue(all(my_utils.get_daily_count(array.array('i',
                                                                 [0, 2, 1]))
                            == array.array('i', [0, 2, 0])))  # exit w/ code 2

    def test_running_avg(self):
        self.assertTrue(all(my_utils.running_average(np.array([0, 1, 2, 3, 4]),
                                                     window=3)
                            == np.array([0., 0.5, 1., 2., 3.])))
        # test when decreasing value
        self.assertTrue(all(my_utils.running_average(np.array([0, 9, 2, 6, 1]),
                                                     window=3)
                            == np.array([0., 4.5, 11./3., 17./3., 3.])))
        # test when window is smaller than length of array
        self.assertTrue(all(my_utils.running_average(np.array([0, 1, 2, 3, 4]),
                                                     window=10)
                            == np.array([0., 0.5, 1., 1.5, 2.])))
        # TODO: include randomness in tests
        # I dont see how to test random w/o writing the whole function here??

        # TODO: test error modes (if any)
        # I dont see how this would have any other error modes


if __name__ == '__main__':
    unittest.main()
