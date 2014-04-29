from __future__ import division 
import requests

# will need to check back regularly to see if this url has changed!
pwt_url = 'http://www.rug.nl/research/ggdc/data/pwt/v80/pwt80.zip'

# Connect to the PWT website...
pwt_buffer = requests.get(url=pwt_url)

# ...save PWT files to disk...
with open('pwt80.zip', 'wb') as pwt_zip_file:
    pwt_zip_file.write(pwt_buffer.content)

