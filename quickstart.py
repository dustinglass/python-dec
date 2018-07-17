from pprint import pprint
from DecCrawler import DecCrawler


QR_CODE = '' # Paste a QR code here


# Instantiate crawler object
dec = DecCrawler()
# Fetch specified QR code page
nfe = dec.get_nfe(QR_CODE)
# Write page data to JSON file
pprint(nfe)
