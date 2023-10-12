import unittest
import datetime as dt
from a4 import *

class TestAux(unittest.TestCase):
    def test_parse_range(self):
        self.assertEqual(parse_range('20200101-31'), ['20200101', '20200131'])

    def test_parse_date_range(self):
        self.assertEqual(parse_date_range('20200101-31'), (20200101, 20200131))
        self.assertEqual(parse_date_range('202001-2'), (20200101, 20200229))
        self.assertEqual(parse_date_range('2020'), (20200101, 20201231))
        self.assertEqual(parse_date_range('2019-22'), (20190101, 20221231))

    def test_parse_date(self):
        self.assertEqual(parse_date('20200101'), 20200101)
        self.assertEqual(parse_date('2020/12-32'), 20201232)
        self.assertEqual(parse_date('2020-02-33'), 20200233)
        now = dt.datetime.now()
        today = now.strftime('%Y%m%d')
        yest  = (now + dt.timedelta(days = -1)).strftime('%Y%m%d')
        tomo5 = (now + dt.timedelta(days =  5)).strftime('%Y%m%d')
        yest2 = (now + dt.timedelta(days = -2)).strftime('%Y%m%d')
        self.assertEqual(parse_date('today', to_str = True), today)
        self.assertEqual(parse_date('yest'), int(yest))
        self.assertEqual(parse_date('yest2'), int(yest2))
        self.assertEqual(parse_date('tomo5'), int(tomo5))
        with self.assertRaises(ValueError):
            parse_date('junk')
        with self.assertRaises(ValueError):
            parse_date('202000111')
        with self.assertRaises(ValueError):
            parse_date('2019')

    def test_parse_url(self):
        self.assertEqual(parse_url(''), {})
        self.assertEqual(parse_url('', abc = 123), {})
        self.assertEqual(parse_url('', proto = 'http'), {'proto': 'http'})
        self.assertEqual(parse_url('', port = 80), {'port': 80})
        self.assertEqual(parse_url('user:p@ss@abc'),
                         {'host': 'abc', 'user': 'user', 'pass': 'p@ss'})
        self.assertEqual(parse_url('user@abc:80'),
                         {'port': 80, 'host': 'abc', 'user': 'user'})
        self.assertEqual(parse_url('abc/a/b/c'),
                         {'host': 'abc', 'path': ['a', 'b', 'c']})
        self.assertEqual(parse_url('abc?a=1,b=2'),
                         {'host': 'abc', 'param': {'a': '1', 'b': '2'}})
        self.assertEqual(parse_url('abc/x/?p=v'),
                         {'host': 'abc', 'path': ['x'], 'param': {'p': 'v'}})
        self.assertEqual(parse_url(':p@ss@quickdb/quick??p=v'),
                         {'user': '', 'pass': 'p@ss', 'host': 'quickdb',
                          'path': ['quick'], 'param': {'?p': 'v'}})
        self.assertEqual(parse_url('u:p@@x.com/path?'),
                         {'user': 'u', 'pass': 'p@', 'host': 'x.com',
                          'path': ['path']})
        self.assertEqual(parse_url('abc?params'), {'host': 'abc'})
        self.assertEqual(parse_url('abc?params,k=v'),
                         {'host': 'abc', 'param': {'k': 'v'}})

    def test_get_opts(self):
        opt, args = get_opts('abc:d:', '-a -c val x y'.split())
        self.assertEqual(opt['a'], True)
        self.assertEqual(opt['b'], False)
        self.assertEqual(opt['c'], 'val')
        self.assertEqual(opt['d'], None)
        self.assertEqual(args, ['x', 'y'])

    def test_parse_opts(self):
        spec = """
-b, --bbb         bool, both
--ccc             bool, long
-d                bool, short
-e, --eee  <int>  arg, both
--fff      <opt>  arg, long
-g         <opt>  arg, short
-h     doc h
--iii  doc iii
-j
--kkk
-l     <arg>
--mmm  <arg>
--no-x
"""
        argv = '-b --kkk --mmm meta --fff=fff -j a b c'.split()
        opt, args = parse_opts(spec, argv)
        self.assertEqual(opt['b'],   True)
        self.assertEqual(opt['bbb'], False)
        self.assertEqual(opt['no-x'], False)
        self.assertEqual(opt['b', 'bbb'], True)
        self.assertEqual(opt['b', 'bbb', 'j'], True)
        self.assertEqual(opt['d', 'ccc'], False)
        self.assertEqual(opt['ccc'], False)
        self.assertEqual(opt['d'],   False)
        self.assertEqual(opt['e'],   None)
        self.assertEqual(opt['eee'], None)
        self.assertEqual(opt['fff'], 'fff')
        self.assertEqual(opt['g'],   None)
        self.assertEqual(opt['h'],   False)
        self.assertEqual(opt['iii'], False)
        self.assertEqual(opt['j'],   True)
        self.assertEqual(opt['kkk'], True)
        self.assertEqual(opt['l'],   None)
        self.assertEqual(opt['mmm'], 'meta')
        self.assertEqual(args, ['a', 'b', 'c'])

        opt, args = parse_opts(spec, ['a', 'b', 'c'])
        self.assertEqual(len(opt), 15)
        self.assertEqual(args, ['a', 'b', 'c'])

        opt, args = parse_opts(spec, [])
        self.assertEqual(len(opt), 15)
        self.assertEqual(args, [])

        opt, args = parse_opts(spec, '-b a b -d'.split())
        self.assertEqual(opt['b'], True)
        self.assertEqual(opt['d'], False)
        self.assertEqual(args, ['a', 'b', '-d'])

        opt, args = parse_opts(spec, '-b a b -d'.split(), greedy=True)
        self.assertEqual(opt['b'], True)
        self.assertEqual(opt['d'], True)
        self.assertEqual(args, ['a', 'b'])

        opt, args = parse_opts(spec, '-b a b -g'.split(), panic=False)
        self.assertEqual(opt['b'], True)
        self.assertEqual(opt['g'], None)
        self.assertEqual(args, ['a', 'b', '-g'])

if __name__ == '__main__':
    unittest.main()
