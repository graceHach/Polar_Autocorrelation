import sys
import unittest
import pandas as pd
sys.path.append("..")
import polarAC_utils as pAC # noqa


class TestUtils(unittest.TestCase):
    def test_sorting(self):
        """
        Sorts bean_df and compares it to a validated dataset (correctly sorted bean)
        tests sortCCW() which uses helper functions return_closest() and
        return_two_closest()
        """
        bean_df = pd.read_csv('data/bean_data.csv')
        # Header  = None prevents first line from being used as a header
        correctly_sorted_bean_df = pd.read_csv('data/sorted_bean.csv', header=None)
        correctly_sorted_bean_tuples = list(correctly_sorted_bean_df.itertuples(index=False, name=None))
        bean_df.columns = ['x', 'y']
        bean_tuples = list(zip(bean_df['x'], bean_df['y']))
        sorted_bean = pAC.sort_CCW(bean_tuples)
        boo_l = [(x,y) for x,y in zip(sorted_bean, correctly_sorted_bean_tuples) if not x==y]
        self.assertTrue(boo_l)  # It's halloween :)

    #def test_autocorreation(self):

    #def

if __name__ == '__main__':
    unittest.main()


