from __future__ import division 
import requests

# will need to check back regularly to see if base url has changed!
base_url = 'http://www.rug.nl/research/ggdc/data/pwt/v80/'

def get_pwt_data(base_url):
    """Downloads the PWT data from the web."""
    file_name = 'pwt.zip'
    pwt_buffer = requests.get(url=base_url + file_name)
    
    with open(file_name, 'wb') as pwt_zip_file:
        pwt_zip_file.write(pwt_buffer.content)

    print(file_name + ' successfully downloaded!')
    
def get_dep_rates_data(base_url):
    """Downloads the data on depreciation rates from the web."""
    file_name = 'depreciation_rates.zip'
    dep_rates_buffer = requests.get(url=base_url + file_name)

    with open('depreciation_rates.zip', 'wb') as dep_rates_zip_file:
        dep_rates_zip_file.write(dep_rates_buffer.content)

    print(file_name + ' successfully downloaded!')
        
if __name__ == '__main__':
    base_url = 'http://www.rug.nl/research/ggdc/data/pwt/v80/'

    get_pwt_data(base_url)
    get_dep_rates_data(base_url)
