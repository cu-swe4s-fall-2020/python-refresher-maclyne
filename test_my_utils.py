"""Testing library of functions in my_utils.py

    Initial date: 1 Oct 2020
    Author: Margot Clyne
    
    Updated Oct 22 get_column to take a list or target columns and return a list of lists

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
                         0, '2020-09-04', result_columns=[4]),
                        [[2399]])
    
    def test_get_column_multipleresultcolumns(self):
        # test that I get what I think for result_columns of len>1
        self.assertEqual(my_utils.get_column(
                        'covid-19-data/us-counties-testfile-Boulder.csv',
                        0, '2020-09-04', result_columns=[4,5]),
                        [[2399],[79]])

    def test_get_column_querynotmatched(self):
        # empty array of int if the query value is not in the file.
        self.assertEqual(my_utils.get_column(
                        'covid-19-data/us-counties-testfile-Boulder.csv',
                         1, 'Denver', result_columns=[4]), [[]])

#    def test_get_column_badfile(self):
#        # error mode raised if file not found
#        self.assertRaises(FileNotFoundError, my_utils.get_column(
#                         'name-of-some-file-that-doesnt-exist-in-path.csv',
#                          0, '2020-09-04', result_columns=[4]))

    def test_get_column_missingdates(self):
        self.assertEqual(my_utils.get_column(
                         'covid-19-data/'
                         + 'us-counties-testfile-Boulder-fakemissingdates.csv',
                         1, 'Boulder', result_columns=[4], date_column=0),
                         [[2289, 2289, 2289, 2324, 2344,
                           2361, 2399, 2399, 2399, 2399,
                           2399, 2574, 2574, 2671]])

    def test_get_column_withdeaths(self):
        # test this works for missing dates and two result_columns 
        self.assertEqual(my_utils.get_column(
                         'covid-19-data/'
                         + 'us-counties-testfile-Boulder-shorter.csv',
                         1, 'Boulder', result_columns=[4,5], date_column=0),
                         [[2289, 2324, 2344, 2361, 2399, 2574, 2671],
                          [79, 79, 79, 80, 80, 81, 83]])

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

    def test_get_daily_count_randomness(self):
        # include randomness in tests
        r1 = random.randint(0, 100)
        r2 = random.randint(0, 100)
        r3 = random.randint(0, 100)
        r4 = random.randint(0, 100)
        cumul_in = array.array('i', [r1, r1+r2, r1+r2+r3, r1+r2+r3+r4])
        daily_out = array.array('i', [r1, r2, r3, r4])
        self.assertTrue(all(my_utils.get_daily_count(cumul_in) == daily_out))

#    def test_get_daily_count_decreasing(self):
#        # test error mode for decreasing cases (exit code 2)
#        with self.assertRaises(ValueError):
#            my_utils.get_daily_count(array.array('i', [0, 2, 1]))

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
