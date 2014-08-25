"""
tests for pypwt.pwt

@author : David R. Pugh
@date : 2014-08-25

"""
from __future__ import division
import unittest

from .. import pwt


class TestPWT(unittest.TestCase):

    data = pwt.PWT()

    def test_validate_index1(self):
        """Test validation of index1 attribute."""
        # index1 must be either 'geks' or 'gk'
        with self.assertRaises(AttributeError):
            self.data.index1 = 'asdf'

        # index1 type must be string
        with self.assertRaises(AttributeError):
            self.data.index1 = None

        # valid setter
        self.data.index1 = 'gk'
        self.assertEquals(self.data.index1, 'gk')

    def test_validate_index2(self):
        """Test validation of index2 attribute."""
        # index2 must be either 'geks' or 'gk'
        with self.assertRaises(AttributeError):
            self.data.index2 = 'asdf'

        # index2 type must be string
        with self.assertRaises(AttributeError):
            self.data.index2 = None

        # valid setter
        self.data.index2 = 'geks'
        self.assertEquals(self.data.index2, 'geks')

    def test_validate_bm(self):
        """Test validation of bm attribute."""
        valid_bms = ['all', 1970, 1975, 1980, 1985, 1996]

        # bm must be either 'all' or [1970, 1980
        with self.assertRaises(AttributeError):
            self.data.bm = 'asdf'

        # bm type must be string
        with self.assertRaises(AttributeError):
            self.data.bm = 2001

        # valid setter
        for bm in valid_bms:
            self.data.bm = bm
            self.assertEquals(self.data.bm, bm)

    def test_validate_chn(self):
        """Test validation of chn attribute."""
        # chn must be either 'pwt' or 'icp'
        with self.assertRaises(AttributeError):
            self.data.chn = 'asdf'

        # chn type must be string
        with self.assertRaises(AttributeError):
            self.data.chn = None

        # valid setter
        self.data.chn = 'icp'
        self.assertEquals(self.data.chn, 'icp')

    def test_validate_norm(self):
        """Test validation of norm attribute."""
        # norm must be either True or False
        with self.assertRaises(AttributeError):
            self.data.norm = 0

        # valid setter
        for norm in [True, False]:
            self.data.norm = norm
            self.assertEquals(self.data.norm, norm)
