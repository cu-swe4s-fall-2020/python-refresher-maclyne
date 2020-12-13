"""Testing hash table functions in hash_table.py

    Initial date: 5 Nov 2020
    Author: Margot Clyne

"""
import unittest
import hash_table
import array
import random
import numpy as np


class TestHash(unittest.TestCase):

    # test hash_ascii_sum
    def test_hash_function_ascii_sum(self):
        h = hash_table.hash_ascii_sum('ABC', 10)  # returns 8
        self.assertEqual((65+66+67) % 10, h)
        # scramble key character order
        h_BCA = hash_table.hash_ascii_sum('BCA', 10)  # returns 8

    # test hash_polynomial_rolling
    def test_hash_function_rolling(self):
        h = hash_table.hash_polynomial_rolling('ABC', 10)  # returns 6
        p = 53
        m = 2**64
        s = ((65 + 66*p + 67 * p**2)) % m
        self.assertEqual(s % 10, h)
        # scramble key character order
        h_BCA = hash_table.hash_polynomial_rolling('BCA', 10)  # returns 2
        s_BCA = ((66 + 67*p + 65 * p**2)) % m
        self.assertEqual(s_BCA % 10, h_BCA)
        self.assertNotEqual(h_BCA, h)

    def test_put_chain_ascii(self):
        t = [[] for i in range(10)]
        # test ascii
        hash_table.put(t, 10, 'ABC', '123', method='ascii')
        self.assertEqual(t[8][0][0], 'ABC')
        self.assertEqual(t[8][0][1], '123')
        # put another key in same location
        hash_table.put(t, 10, 'BCA', '456', method='ascii')
        self.assertEqual(t[8][1][0], 'BCA')
        self.assertEqual(t[8][1][1], '456')

    def test_put_chain_rolling(self):
        t = [[] for i in range(10)]
        # test rolling hash
        hash_table.put(t, 10, 'ABC', '789')  # method='rolling'
        self.assertEqual(t[6][0][0], 'ABC')
        self.assertEqual(t[6][0][1], '789')
        # put scrambled key char order
        hash_table.put(t, 10, 'BCA', '101112')
        self.assertEqual(t[2][0][0], 'BCA')
        self.assertEqual(t[2][0][1], '101112')

    def test_get_chain_ascii(self):
        # first put in things to hash table for testing
        t = [[] for i in range(10)]
        hash_table.put(t, 10, 'ABC', '123', method='ascii')
        # test get
        self.assertEqual(hash_table.get(t, 10, 'ABC', method='ascii'), '123')
        # put another key into table at same location for testing
        hash_table.put(t, 10, 'BCA', '456', method='ascii')
        # test get same location different query_key
        self.assertEqual(hash_table.get(t, 10, 'BCA', method='ascii'), '456')
        # test get nonexistent query_key
        self.assertEqual(hash_table.get(t, 10, 'Margot', method='ascii'), None)

    def test_get_chain_rolling(self):
        # first put in things to hash table for testing
        t = [[] for i in range(10)]
        hash_table.put(t, 10, 'ABC', '789')  # method='rolling'
        self.assertEqual(hash_table.get(t, 10, 'ABC'), '789')
        # try put another in same key location different value
        hash_table.put(t, 10, 'ABC', '101112')  # replacing should fail
        self.assertNotEqual(hash_table.get(t, 10, 'ABC'), '101112')


if __name__ == '__main__':
    unittest.main()
