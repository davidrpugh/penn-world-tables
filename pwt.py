from __future__ import division 
from StringIO import StringIO 
import zipfile

import pandas as pd
import requests

# will need to check back regularly to see if base url has changed!
base_url = 'http://www.rug.nl/research/ggdc/data/pwt/v80/'

def get_pwt_data(base_url):
    """Downloads the PWT data from the web."""
    file_names = ['pwt80', 'depreciation_rates']
    
    for file_name in file_names:
        tmp_buffer = requests.get(url=base_url + file_name + '.zip')
        tmp_zip = zipfile.ZipFile(StringIO(tmp_buffer.content))
        tmp_zip.extract(file_name + '.dta')
        print(file_name + ' successfully downloaded!')
 
def load_pwt_data(base_url='http://www.rug.nl/research/ggdc/data/pwt/v80/', version=80):
    """
    Load the Penn World Tables data as a Pandas Panel object.

    Arguments:
 
        base_url (str) Base url to use for the download.
        version: (int) Version number for PWT data. Default is 80 (which is the 
                  most recent version).
                                    
    Returns:

        pwt:    A Pandas Panel object containing the Penn World Tables data.
        
    TODO: Work out a way to merge Pandas Panel objects.
    
    """        
    # first check for a local copy of PWT
    try: 
        pwt_raw_data = pd.read_stata('pwt' + str(version) + '.dta')
        dep_rates_raw_data = pd.read_stata('depreciation_rates.dta')
        
    # otherwise, 
    except IOError:  
        get_pwt_data(base_url)
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
    base_url = 'http://www.rug.nl/research/ggdc/data/pwt/v80/'

    #get_pwt_data(base_url)
    
    pwt_data = load_pwt_data(base_url, version=80)
