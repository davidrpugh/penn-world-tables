from __future__ import division 
import requests

# will need to check back regularly to see if base url has changed!
base_url = 'http://www.rug.nl/research/ggdc/data/pwt/v80/'

# Connect to the PWT data...
pwt_buffer = requests.get(url=base_url + 'pwt.zip')

# ...save PWT files to disk...
with open('pwt80.zip', 'wb') as pwt_zip_file:
    pwt_zip_file.write(pwt_buffer.content)

# Connect to the depreciation rates data...
dep_rates_buffer = requests.get(url=base_url + 'depreciation_rates.zip')

# ...save depreciation rates files to disk...
with open('depreciation_rates.zip', 'wb') as dep_rates_zip_file:
    dep_rates_zip_file.write(dep_rates_buffer.content)
