from __future__ import division 
import requests

# will need to check back regularly to see if this url has changed!
pwt_url = 'http://www.rug.nl/research/ggdc/data/pwt/v80/pwt80.zip'

# Connect to the PWT website...
pwt_buffer = requests.get(url=pwt_url)

# ...save PWT files to disk...
with open('pwt80.zip', 'wb') as pwt_zip_file:
    pwt_zip_file.write(pwt_buffer.content)

dep_rates_url = 'http://www.rug.nl/research/ggdc/data/pwt/v80/depreciation_rates.zip'

# Connect to the depreciation rates data...
dep_rates_buffer = requests.get(url=dep_rates_url)

# ...save depreciation rates files to disk...
with open('depreciation_rates.zip', 'wb') as dep_rates_zip_file:
    dep_rates_zip_file.write(dep_rates_buffer.content)
