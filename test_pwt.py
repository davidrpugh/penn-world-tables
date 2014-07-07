"""Unit testing framework for pwt.py module."""
import os
from nose import with_setup

import pwt


def setup_func(version=80):
    """Setup load_pwt_data test fixture."""
    if os.path.isfile('depreciation_rates.dta'):
        os.remove('depreciation_rates.dta')
    if os.path.isfile('pwt' + str(version) + '.dta'):
        os.remove('pwt' + str(version) + '.dta')


def teardown_func(version=80):
    """Teardown for load_pwt_data test fixture."""
    os.remove('depreciation_rates.dta')
    os.remove('pwt' + str(version) + '.dta')


@with_setup(setup_func, teardown_func)
def test_load_pwt_data(version=80):
    """Test load_pwt_data function."""
    data = pwt.load_pwt_data(base_url='http://www.rug.nl/research/ggdc/data/pwt/',
                             version=version)

    # assert that files have been downloaded
    mesg = "Download of 'depreciation_rates.dta' file failed!"
    assert os.path.isfile('depreciation_rates.dta'), mesg
    mesg = "Download of " + 'pwt' + str(version) + '.dta' + "file failed!"
    assert os.path.isfile('pwt' + str(version) + '.dta'), mesg
