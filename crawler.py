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
        html = r2.text
        tuples = html_to_tuples(html)
        dict_ = tuples_to_dict(tuples)
        self.page = {
                'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                'qr_code': qr_code,
                'data': dict_
            }

def html_to_tuples(html):

    result = []
    soup = BeautifulSoup(html, 'lxml')

    for tag in soup.find_all(['span', 'img']):

        if tag.name == 'span':         
            t1 = tag.string
            if tag.get('class') == ['TituloAreaRestrita']:
                if tag.string.strip() in HEADINGS_3:
                    t0 = 'heading3'
                elif tag.string.strip() in HEADINGS_2:
                    t0 = 'heading2'
                else:
                    t0 = 'heading1'
            elif tag.get('class') == ['TextoFundoBrancoNegrito']:
                t0 = 'field'
            elif tag.get('class') == ['linha']:
                t0 = 'value'
            if t0 in ['field', 'heading1', 'heading2', 'heading3']:
                try:
                    t1 = truncate_whitespace(unidecode(t1)).lower() \
                                                           .replace(' ', '_')
                except:
                    continue
            try:
                t1 = truncate_whitespace(t1)
            except: 
                continue
            result.append((t0, t1))

        elif tag.name == 'img' and tag.get('title') == 'Detalhar':
            result.append(('heading2', tag.next_element))

    return result

def tuples_to_dict(tuples):

    result = {}
    data = {}

    heading1 = None
    heading2 = None
    heading3 = None
    field = None
    value = None

    for t in tuples:

        if t[0] == 'heading1':
            result = {**result, **data}
            data = {}
            heading1 = t[1]
            data[heading1] = {}
            heading2 = None
            heading3 = None
            field = None
            value = None
        elif t[0] == 'heading2':
            heading2 = t[1]
            data[heading1][heading2] = {}
            heading3 = None
        elif t[0] == 'heading3':
            heading3 = t[1]
            data[heading1][heading2][heading3] = {}
        elif t[0] == 'field':
            field = t[1]
            value = None
        elif t[0] == 'value':
            value = t[1]
        if field and value:
            if heading3:
                data[heading1][heading2][heading3][field] = value
            elif heading2:
                data[heading1][heading2][field] = value
            elif heading1:
                data[heading1][field] = value
            else:
                data[field] = value

    return result
