from requests import session
from datetime import datetime
from NfeParser import NfeParser


BASE_URL = 'http://dec.fazenda.df.gov.br/'
EXT1 = 'ConsultarNFCe.aspx?chNFe='
EXT2 = 'autoUso.aspx?cmd=9&doc='


class DecCrawler:

    def __init__(self, url=BASE_URL, ext1=EXT1, ext2=EXT2):

        self._session = session()
        self._url = url
        self._ext1 = ext1
        self._ext2 = ext2

    def get_nfe(self, qr_code):
        
        if not qr_code.startswith(self._url + self._ext1):
            raise ValueError
        # Connect session to website
        r1 = self._session.get(qr_code)
        # Store response from next page in session
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        r2 = self._session.get(self._url + self._ext2)
        return {
            'timestamp': timestamp,
            'qr_code': qr_code,
            'status_code': r2.status_code,
            'data': NfeParser(r2.text).data
        }
