import unittest
import os
import shutil

from aistac.components.aistac_commons import DataAnalytics, AistacCommons
from aistac.properties.property_manager import PropertyManager


class CommonsTest(unittest.TestCase):

    def setUp(self):
        os.environ['HADRON_PM_PATH'] = os.path.join('work', 'config')
        os.environ['HADRON_DEFAULT_PATH'] = os.path.join('work', 'data')
        try:
            os.makedirs(os.environ['HADRON_PM_PATH'])
            os.makedirs(os.environ['HADRON_DEFAULT_PATH'])
        except:
            pass
        PropertyManager._remove_all()

    def tearDown(self):
        try:
            shutil.rmtree('work')
        except:
            pass

    def test_list_formatter(self):
        sample = {'A': [1,2], 'B': [1,2], 'C': [1,2]}
        result = AistacCommons.list_formatter(sample)
        self.assertEqual(list("ABC"), result)
        result = AistacCommons.list_formatter(sample.keys())
        self.assertEqual(list("ABC"), result)
        result = AistacCommons.list_formatter("A")
        self.assertEqual(['A'], result)

    def test_list_standardize(self):
        seq = [100, 75, 50, 25, 0]
        result = AistacCommons.list_standardize(seq=seq)
        self.assertEqual(0.0, result[2])
        self.assertEqual(0.0, result[1] + result[3])
        self.assertEqual(0.0, result[0] + result[4])

    def test_list_normalize(self):
        seq = [100, 75, 50, 25, 0]
        a = 0
        b = 1
        result = AistacCommons.list_normalize(seq=seq, a=a, b=b)
        self.assertEqual([1.0, 0.75, 0.5, 0.25, 0.0], result)
        a = -1
        b = 1
        result = AistacCommons.list_normalize(seq=seq, a=a, b=b)
        self.assertEqual([1.0, 0.5, 0, -0.5, -1], result)

    def test_diff(self):
        a = [1,2,3,4]
        b = [2,3,4,6,7]
        self.assertEqual([1, 6, 7], AistacCommons.list_diff(a, b))
        self.assertEqual([1], AistacCommons.list_diff(a, b, symmetric=False))

    def test_is_list_equal(self):
        a = [1, 4, 2, 1, 4]
        b = [4, 2, 4, 1, 1]
        self.assertTrue(AistacCommons.list_equal(a, b))
        b = [4, 2, 4, 2, 1]
        self.assertFalse(AistacCommons.list_equal(a, b))

    def test_resize_list(self):
        seq = [1,2,3,4]
        for size in range(10):
            result = AistacCommons.list_resize(seq=seq, resize=size)
            self.assertEqual(size, len(result))
            if len(result) >= 4:
                self.assertEqual(seq, AistacCommons.list_unique(result))

    def test_dict_builder(self):
        result = AistacCommons.param2dict()
        self.assertEqual({}, result)
        result = AistacCommons.param2dict(a=1, b='B')
        self.assertEqual({'a': 1, 'b': 'B'}, result)
        result = AistacCommons.param2dict(a=1, b=[1,2,3])
        self.assertEqual({'a': 1, 'b': [1, 2, 3]}, result)
        result = AistacCommons.param2dict(a={'A': 1})
        self.assertEqual({'a': {'A': 1}}, result)
        result = AistacCommons.param2dict(a=1, b=None)
        self.assertEqual({'a': 1}, result)

    def test_dict_with_missing(self):
        default = 'no value'
        sample = AistacCommons.dict_with_missing({}, default)
        result = sample['key']
        self.assertEqual(default, result)

    def test_bytestohuman(self):
        result = AistacCommons.bytes2human(1024)
        self.assertEqual('1.0KB', result)
        result = AistacCommons.bytes2human(1024**2)
        self.assertEqual('1.0MB', result)
        result = AistacCommons.bytes2human(1024**3)
        self.assertEqual('1.0GB', result)

    def test_validate_date(self):
        str_date = '2017/01/23'
        self.assertTrue(AistacCommons.valid_date(str_date))
        str_date = '2017/23/01'
        self.assertTrue(AistacCommons.valid_date(str_date))
        str_date = '23-01-2017'
        self.assertTrue(AistacCommons.valid_date(str_date))
        str_date = '01-21-2017'
        self.assertTrue(AistacCommons.valid_date(str_date))
        str_date = 'NaT'
        self.assertFalse(AistacCommons.valid_date(str_date))
        str_date = ''
        self.assertFalse(AistacCommons.valid_date(str_date))
        str_date = '01-21-2017 21:12:46'
        self.assertTrue(AistacCommons.valid_date(str_date))

    def test_analytics(self):
        analysis = {'intent': {'categories': ['a', 'b'], 'dtype': 'category'},
                    'patterns': {'relative_freq': [.6, .4], 'unique_count': 2}}
        result = DataAnalytics(analysis)
        self.assertEqual(['a', 'b'], result.get('intent').get('categories', []))
        self.assertEqual([], result.get('no_name', []))
        self.assertEqual({}, result.get('no_name'))
        self.assertEqual(['a', 'b'], result.intent.categories)
        self.assertEqual('category', result.intent.dtype)
        self.assertEqual(['categories', 'dtype'], result.intent.elements())

    def test_build_category(self):
        result = DataAnalytics.build_category(header='gender', lower=0.1, nulls_list=['', ' '])
        self.assertEqual({'gender': {'lower': 0.1, 'nulls_list': ['', ' ']}}, result)

    def test_raise(self):
        with self.assertRaises(KeyError) as context:
            env = os.environ['NoEnvValueTest']
        self.assertTrue("'NoEnvValueTest'" in str(context.exception))


if __name__ == '__main__':
    unittest.main()
