from __future__ import division 
import zipfile

import pandas as pd
import requests

# will need to check back regularly to see if base url has changed!
base_url = 'http://www.rug.nl/research/ggdc/data/pwt/v80/'

def get_pwt_data(base_url):
    """Downloads the PWT data from the web."""
    file_names = ['pwt80.zip', 'depreciation_rates.zip']
    
    for file_name in file_names:
        tmp_buffer = requests.get(url=base_url + file_name)
    
        with open(file_name, 'wb') as tmp_zip_file:
            tmp_zip_file.write(tmp_buffer.content)

        print(file_name + ' successfully downloaded!')
 
tmp_buffer = zipfile.ZipFile('pwt80.zip')
tmp_buffer.extract('pwt80.dta')
tmp_dataframe = pd.read_stata('pwt80.dta')          

tmp_buffer = zipfile.ZipFile('depreciation_rates.zip')
tmp_buffer.extract('depreciation_rates.dta')
tmp_dataframe = pd.read_stata('depreciation_rates.dta')          

if __name__ == '__main__':
    base_url = 'http://www.rug.nl/research/ggdc/data/pwt/v80/'

    get_pwt_data(base_url)
