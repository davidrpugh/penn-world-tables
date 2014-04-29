from __future__ import division 
from StringIO import StringIO 
import zipfile

import pandas as pd
import requests

# will need to check back regularly to see if base url has changed!
base_url = 'http://www.rug.nl/research/ggdc/data/pwt/'

def download_dep_rates_data(base_url, version=80):
    """Downloads the depreciation rate data."""
    tmp_url = base_url + 'v' + str(version) + '/depreciation_rates.zip'
    tmp_buffer = requests.get(url=tmp_url)
    tmp_zip = zipfile.ZipFile(StringIO(tmp_buffer.content))
    tmp_zip.extract('depreciation_rates.dta')

def download_pwt_data(base_url, version=80):
    """Downloads the Penn World Tables (PWT) data."""
    tmp_url = base_url + 'v' + str(version) + '/pwt' + str(version) + '.zip'
    tmp_buffer = requests.get(url=tmp_url)
    tmp_zip = zipfile.ZipFile(StringIO(tmp_buffer.content))
    tmp_zip.extract('pwt' + str(version) + '.dta')
     
def load_pwt_data(base_url='http://www.rug.nl/research/ggdc/data/pwt', version=80):
    """
    Load the Penn World Tables data as a Pandas Panel object.

    Arguments:
 
        base_url (str) Base url to use for the download.
        version: (int) Version number for PWT data. Default is 80 (which is the 
                  most recent version).
                                    
    Returns:

        pwt:    A Pandas Panel object containing the Penn World Tables data.
            
    """        
    try: 
        pwt_raw_data = pd.read_stata('pwt' + str(version) + '.dta')
        dep_rates_raw_data = pd.read_stata('depreciation_rates.dta')
        
    except IOError:  
        download_pwt_data(base_url, version)
        download_dep_rates_data(base_url, version)
        
        pwt_raw_data = pd.read_stata('pwt' + str(version) + '.dta')
        dep_rates_raw_data = pd.read_stata('depreciation_rates.dta')
        
    # merge the data
    pwt_merged_data = pd.merge(pwt_raw_data, dep_rates_raw_data, how='outer', 
                               on=['countrycode', 'year'])

    # coerce into a Pandas panel
    pwt_merged_data.set_index(['countrycode', 'year'], inplace=True)
    pwt_panel_data = pwt_merged_data.to_panel()

    return pwt_panel_data
        
if __name__ == '__main__':
    base_url = 'http://www.rug.nl/research/ggdc/data/pwt/'

    #download_pwt_data(base_url)
    #download_dep_rates_data(base_url)
    pwt_data = load_pwt_data(base_url, version=80)
