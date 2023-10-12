import unittest
from dux.cal import *

class TestBizday(unittest.TestCase):
    def test_url_mkt2cal(self):
        self.assertEqual(mkt2cal(1), 86)

    def test_bizday(self):
        self.assertEqual(bizday(20220101), False)
        self.assertEqual(bizday(20220104), True)
        self.assertEqual(bizday(20220101, 10), 20220117)
        self.assertEqual(bizday('20220101', 10), 20220117)

    def test_bizdays(self):
        self.assertEqual(bizdays(20220101, 20220105), [20220104, 20220105])
        self.assertEqual(bizdays(20220101), [])
        self.assertEqual(bizdays('20220101-5'), [20220104, 20220105])
        self.assertEqual(bizdays('19901219-20'), [19901219, 19901220])
        with self.assertRaises(ValueError):
            bizdays('19901219-20-x')
        with self.assertRaises(ValueError):
            bizdays('1990-202012')

    def test_caldays(self):
        self.assertEqual(len(caldays('20220101-10')), 10)
        with self.assertRaises(ValueError):
            caldays('19901239-40')

    def test_shift(self):
        self.assertEqual(calday(20210211, '1d'),  20210212)
        self.assertEqual(calday(20210211, '-1w'), 20210204)
        self.assertEqual(calday(20210211, '-1w'), 20210204)
        self.assertEqual(calday(20201231, '1y'),  20211231)
        self.assertEqual(stride(20201231, '1y'),  20211231)
        self.assertEqual(stride_back(20211231, '1y'),  20201231)
        self.assertEqual(calday(20200101, '1y'), 20210101)
        self.assertEqual(stride(20200101, '1y'), 20201231)
        self.assertEqual(stride(20210101, '-1y'), 20200102)
        self.assertEqual(stride(20120228, '23M'), 20140128)

if __name__ == '__main__':
    unittest.main()
