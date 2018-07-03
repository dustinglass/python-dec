#!/usr/bin/python3
# -*- coding: utf-8 -*- 

import requests
from datetime import datetime
from utils import *

BASE_URL = 'http://dec.fazenda.df.gov.br/'
EXT1 = 'ConsultarNFCe.aspx?chNFe='
EXT2 = 'autoUso.aspx?cmd=9&doc='

class OnlineNFCrawler(object):

    def __init__(self, url=BASE_URL, ext1=EXT1, ext2=EXT2):

        self._session = requests.session()
        self._url = url
        self._ext1 = ext1
        self._ext2 = ext2
        self.page = None

    def get_page(self, qr_code):
        
        if not qr_code.startswith(self._url + self._ext1):
            raise ValueError
        # Connect session to website
        r1 = self._session.get(qr_code)
        print(r1.status_code)
        # Store response from next page in session
        r2 = self._session.get(self._url + self._ext2)
        print(r2.status_code)
        self.page = {
                'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                'qr_code': qr_code,
                'status': r2.status_code,
                'html': r2.text
            }
