# python-dec
Use this module to scrape an electronic receipt (nota fiscal eletrônica) from http://dec.fazenda.df.gov.br/.

The DecCrawler class can take a QR code scanned from a printed receipt in Brazil and return detailed data from the electronic receipt as a Python dict with its get_nfe() method. Currently we only have support for the Federal District (Distrito Federal).

## Quickstart
To demonstrate python-dec's functionality, scan a QR code from a receipt you have available and insert it into the following script:
```
from pprint import pprint
from DecCrawler import DecCrawler


QR_CODE = '' # Paste a QR code here


dec = DecCrawler() # Instantiates a crawler object
nfe = dec.get_nfe(QR_CODE) # Fetches the specified QR code page
pprint(nfe) # Pretty prints the data object generated from the QR code
```
