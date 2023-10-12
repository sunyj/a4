import unittest
import dux.secdb as sdb


class TestSecDB(unittest.TestCase):
    def test_mkt_univ(self):
        mkt = sdb.mkt_info(1)
        self.assertEqual(mkt.name, 'cneq')

        mkt = sdb.mkt_info('cneq')
        self.assertEqual(mkt.id,   1)
        self.assertEqual(mkt.name, 'cneq')
        self.assertEqual(mkt.tz,   'PRC')

        univ = sdb.univ_info(mkt.univ)
        self.assertEqual(mkt.univ, univ.id)
        self.assertEqual(univ.mkt, mkt.id)

        cne = sdb.univ_info('cne')
        self.assertEqual(cne.mkt, mkt.id)

    def test_freq(self):
        with self.assertRaises(ValueError):
            self.assertEqual(sdb.freq_secs('M10', 'nil'), [])
        m10 = sdb.freq_secs('M10')
        self.assertEqual(len(m10), 24)
        self.assertEqual(m10[0],   34800)
        self.assertEqual(m10[-1],  54000)
        self.assertEqual(sdb.freq_secs('nil'), [])

    def test_xid(self):
        # common stock
        self.assertEqual(sdb.xid(0),            "")
        self.assertEqual(sdb.xid(-1),           "")
        self.assertEqual(sdb.xid(""),           0)
        self.assertEqual(sdb.xid(None),         0)
        self.assertEqual(sdb.xid("nil"),        0)
        self.assertEqual(sdb.xid(1),            "000005.SZ")
        self.assertEqual(sdb.xid("000005.SZ"),  1)
        self.assertEqual(sdb.xid("600001.SH"),  726)
        # symbol change
        self.assertEqual(sdb.xid(83),           "001872.SZ")
        self.assertEqual(sdb.xid(83, 20181225), "001872.SZ")
        self.assertEqual(sdb.xid(83, 20181224), "000022.SZ")

        # Index
        self.assertEqual(sdb.xid("000001.SH"),  134217729)
        self.assertEqual(sdb.xid("399999.SZ"),  151394943)
        self.assertEqual(sdb.xid(134217729),    "000001.SH")
        self.assertEqual(sdb.xid(151394943),    "399999.SZ")

        # ETF
        self.assertEqual(sdb.xid("512345.SH"),  470274393)
        self.assertEqual(sdb.xid("156789.SZ"),  486696053)
        self.assertEqual(sdb.xid(470274393),    "512345.SH")
        self.assertEqual(sdb.xid(486696053),    "156789.SZ")

        # CB
        self.assertEqual(sdb.xid("111111.SH"),  536982023)
        self.assertEqual(sdb.xid("121111.SZ"),  553769239)
        self.assertEqual(sdb.xid("111111.sh"),  0)
        self.assertEqual(sdb.xid("121111.sz"),  0)
        self.assertEqual(sdb.xid("111111.SHE"), 0)
        self.assertEqual(sdb.xid("1211111.SZ"), 0)
        self.assertEqual(sdb.xid(536982023),    "111111.SH")
        self.assertEqual(sdb.xid(553769239),    "121111.SZ")
        self.assertEqual(sdb.xid(999999999),    "")
        self.assertEqual(sdb.xid(536980912),    "110000.SH")
        self.assertEqual(sdb.xid(537000911),    "")
        self.assertEqual(sdb.xid(553758128),    "")
        self.assertEqual(sdb.xid(553778127),    "129999.SZ")
        self.assertEqual(sdb.xid(553778128),    "")

    def test_univ(self):
        self.assertTrue(sdb.univ_sids('alev', 20200104))
        self.assertTrue(sdb.univ_sids('ZZ1000', 20200104))

        self.assertTrue(sdb.univ_sids('cne', 20200104))
        self.assertTrue(isinstance(sdb.univ_sids('cne', 20200104), list))
        self.assertEqual(len(sdb.univ_sids('cne', '20200104')), 3760)
        self.assertEqual(len(sdb.univ_sids('cne', '202001')), 3776)
        self.assertEqual(len(sdb.univ_sids('cne', 20200101, 20200131)), 3776)

        self.assertTrue(sdb.univ_syms('cne', 20200104))
        self.assertTrue(isinstance(sdb.univ_syms('cne', 20200104), dict))
        self.assertEqual(len(sdb.univ_syms('cne', '20200104')), 3760)
        self.assertEqual(len(sdb.univ_syms('cne', '202001')), 3776)
        self.assertEqual(len(sdb.univ_syms('cne', 20200101, 20200131)), 3776)

    def test_cneq_attr(self):
        attr = sdb.cneq_attr(3456)
        self.assertEqual(attr.sid, 3456)
        self.assertEqual(attr.sym, "603321.SH")

        attr = sdb.cneq_attr(3456, 20150101)
        self.assertEqual(attr.sid, 0)
        self.assertEqual(attr.sym, "")

        self.assertEqual(sdb.cneq_attr(2399, 20180101).sym, "601313.SH")
        self.assertEqual(sdb.cneq_attr(2399, 20200101).sym, "601360.SH")

        attr = sdb.cneq_attr(1811)
        self.assertEqual(attr.since, 20100210)
        self.assertEqual(attr.until, 20210722)
        attr = sdb.cneq_attr(1811, 20100101)
        self.assertEqual(attr.since, 0)
        self.assertEqual(attr.until, 0)
        attr = sdb.cneq_attr(1811, 20200101)
        self.assertEqual(attr.since, 20100210)
        self.assertEqual(attr.until, 0)

    def test_cneq(self):
        self.assertTrue(sdb.cneq())
        self.assertTrue(13 not in sdb.cneq(20220101))
        self.assertTrue('000003.SZ' not in sdb.cneq(20220101, symbolic = True))
        self.assertTrue(13 in sdb.cneq(20220101, full = True))
        self.assertFalse(sdb.cneq(20220101)[1].normal)
        self.assertTrue(sdb.cneq(20220101)[10].normal)
        self.assertEqual(len(sdb.cneq(20220101)), 4602)
        rec = sdb.cneq(20220101)[1]
        self.assertEqual(rec.sym, "")
        self.assertEqual(rec.since, 19901219)
        self.assertEqual(rec.until, 0)
        rec = sdb.cneq(20220101, symbolic=True)['000005.SZ']
        self.assertEqual(rec.sid, 1)
        self.assertEqual(rec.since, 19901219)
        self.assertEqual(rec.until, 0)


if __name__ == '__main__':
    unittest.main()
