"""Unit testing framework for pwt.py module."""
import os
import unittest

import pwt


class TestPWTDownload(unittest.TestCase):

    base_url = 'http://www.rug.nl/research/ggdc/data/pwt/'

    version = 80

    def setUp(self):
        """Setup test fixtures."""
        files = ['depreciation_rates.dta', 'pwt' + str(self.version) + '.dta']

        for tmp_file in files:
            if os.path.isfile(tmp_file):
                os.remove(tmp_file)

    def tearDown(self):
        """Teardown for load_pwt_data test fixture."""
        self.setUp()

    def test__get_dep_rates_data(self):
        pwt._get_dep_rates_data(self.base_url, self.version)

        # assert that files have been downloaded
        mesg = "Download of 'depreciation_rates.dta' file failed!"
        assert os.path.isfile('depreciation_rates.dta'), mesg

# def test__get_pwt_data(base_url='http://www.rug.nl/research/ggdc/data/pwt/', version=80):
#     """Test load_pwt_data function."""
#     pwt._get_pwt_data(base_url, version)

#     # assert that files have been downloaded
#     mesg = "Download of " + 'pwt' + str(version) + '.dta' + "file failed!"
#     assert os.path.isfile('depreciation_rates.dta'), mesg

# @with_setup(setup_func, teardown_func)
# def test_load_pwt_data(version=80):
#     """Test load_pwt_data function."""
#     data = pwt.load_pwt_data(base_url='http://www.rug.nl/research/ggdc/data/pwt/',
#                              version=version)

#     # assert that files have been downloaded
#     mesg = "Download of 'depreciation_rates.dta' file failed!"
#     assert os.path.isfile('depreciation_rates.dta'), mesg
#     mesg = "Download of " + 'pwt' + str(version) + '.dta' + "file failed!"
#     assert os.path.isfile('pwt' + str(version) + '.dta'), mesg
