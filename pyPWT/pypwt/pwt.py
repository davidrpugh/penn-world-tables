"""Module for downloading the Penn World Tables (PWT) data.

Module contains a set of functions that download the PWT data set and coerce
it into a Pandas Panel object for subsequent analysis.

"""
from __future__ import division
from StringIO import StringIO
import zipfile

import pandas as pd
import requests


def _get_dep_rates_data(base_url, version):
    """Download the depreciation rate data."""
    tmp_url = base_url + 'v' + str(version) + '/depreciation_rates.zip'
    tmp_buffer = requests.get(url=tmp_url)
    tmp_zip = zipfile.ZipFile(StringIO(tmp_buffer.content))
    tmp_zip.extract('depreciation_rates.dta')


def _get_pwt_data(base_url, version):
    """Download the Penn World Tables (PWT) data."""
    tmp_url = base_url + 'v' + str(version) + '/pwt' + str(version) + '.zip'
    tmp_buffer = requests.get(url=tmp_url)
    tmp_zip = zipfile.ZipFile(StringIO(tmp_buffer.content))
    tmp_zip.extract('pwt' + str(version) + '.dta')


def _download_pwt_data(base_url, version):
    """Download the Penn World Tables (PWT) data."""
    _get_dep_rates_data(base_url, version)
    _get_pwt_data(base_url, version)


def load_pwt_data(base_url='http://www.rug.nl/research/ggdc/data/pwt/',
                  version=80):
    """
    Load the Penn World Tables (PWT) data as a Pandas Panel object.

    Parameters
    ----------
        base_url : str, optional(default='http://www.rug.nl/research/ggdc/data/pwt/')
            Base url to use for the download.
        version : int, optional(default=80)
            Version number for PWT data.

    Returns
    -------
        pwt_panel_data : pd.Panel
            A Pandas Panel object containing the Penn World Tables (PWT) data.

    """
    try:
        pwt_raw_data = pd.read_stata('pwt' + str(version) + '.dta')
        dep_rates_raw_data = pd.read_stata('depreciation_rates.dta')

    except IOError:
        _download_pwt_data(base_url, version)
        pwt_raw_data = pd.read_stata('pwt' + str(version) + '.dta')
        dep_rates_raw_data = pd.read_stata('depreciation_rates.dta')

    # merge the data
    pwt_merged_data = pd.merge(pwt_raw_data, dep_rates_raw_data, how='outer',
                               on=['countrycode', 'year'])

    # create the hierarchical index
    pwt_merged_data.year = pd.to_datetime(pwt_raw_data.year, format='%Y')
    pwt_merged_data.set_index(['countrycode', 'year'], inplace=True)

    # coerce into a panel
    pwt_panel_data = pwt_merged_data.to_panel()

    return pwt_panel_data
