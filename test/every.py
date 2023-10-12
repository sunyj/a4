import unittest
from dux.cal import *
from dux.aux import *

class TestBizday(unittest.TestCase):
    def test_every_day(self):
        self.assertEqual(parse_cron_dates('day', '202201'), bizdays('20220101-31'))
        self.assertEqual(parse_cron_dates('day', '20100101-3'), [])

    def test_every_week(self):
        self.assertEqual(parse_cron_dates('Mon of week', '202201'),
                         [20220104, 20220110, 20220117, 20220124])
        self.assertEqual(parse_cron_dates('Fri of week', '20210210-20'),
                         [20210218])
        self.assertEqual(parse_cron_dates('Tue of week', '202210'),
                         [20221010, 20221018, 20221025])

    def test_every_month(self):
        self.assertEqual(parse_cron_dates('15th of Jan', '2012-15'),
                         [20120116, 20130115, 20140115, 20150115])
        self.assertEqual(
            parse_cron_dates('15th of month', '2020', since=20201001),
            [20201015, 20201116, 20201215])

if __name__ == '__main__':
    unittest.main()
