#!/usr/bin/python3
# -*- coding: utf-8 -*- 

import requests
from datetime import datetime
from bs4 import BeautifulSoup
from utils import *

BASE_URL = 'http://dec.fazenda.df.gov.br/'
EXT1 = 'ConsultarNFCe.aspx?chNFe='
EXT2 = 'autoUso.aspx?cmd=9&doc='
HEADINGS_2 = [
    'IMPOSTO SOBRE CIRCULAÇÃO DE MERCADORIAS E SERVIÇOS (ICMS)',
    'IMPOSTO SOBRE SERVIÇOS DE QUALQUER NATUREZA (ISSQN)',
    'Formas de Pagamento',
    'id'
]
HEADINGS_3 = [
    'ICMS NORMAL E ST',
    'PROGRAMA DE INTEGRAÇÃO SOCIAL (PIS)',
    'CONTRIBUIÇÃO PARA FINANCIAMENTO DA SEGURIDADE SOCIAL (COFINS)'
]

class DEC:

    def __init__(self, url=BASE_URL, ext1=EXT1, ext2=EXT2):

        self._session = requests.session()
        self._url = url
        self._ext1 = ext1
        self._ext2 = ext2

    def get_nfe(self, qr_code):
        
        if not qr_code.startswith(self._url + self._ext1):
            raise ValueError
        # Connect session to website
        r1 = self._session.get(qr_code)
        # Store response from next page in session
        r2 = self._session.get(self._url + self._ext2)
        return {'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                'qr_code': qr_code,
                'status': r2.status_code,
                'data': tuples_to_dict(html_to_tuples(r2.text))
            }

def html_to_tuples(html):

    result = []
    soup = BeautifulSoup(html, 'lxml')

    for tag in soup(['span', 'img']):

        if tag.name == 'span':         
            t1 = tag.string
            if tag.get('class') == ['TituloAreaRestrita']:
                if t1.strip() in HEADINGS_3:
                    t0 = 'heading_3'
                elif t1.strip() in HEADINGS_2:
                    t0 = 'heading_2'
                else:
                    t0 = 'heading_1'
            elif tag.get('class') == ['TextoFundoBrancoNegrito']:
                t0 = 'field'
            elif tag.get('class') == ['linha']:
                t0 = 'value'
            try:
                t1 = truncate_whitespace(t1)
            except: 
                continue
            if t0 != 'value':
                t1 = standardize(normalize(t1))
                print(t1)
                print(type(t1))
            result.append((t0, t1))

        elif tag.name == 'img' and tag.get('title') == 'Detalhar':
            result.append(('heading_2', tag.next_element))

    return result

def tuples_to_dict(tuples):

    result = {}
    data = {}
    heading_1 = None
    heading_2 = None
    heading_3 = None
    field = None
    value = None

    for t in tuples:

        if t[0] == 'heading_1':
            result = {**result, **data}
            data = {}
            heading_1 = t[1]
            data[heading_1] = {} 
            heading_2 = None
            heading_3 = None
            field = None
            value = None
        elif t[0] == 'heading_2':
            heading_2 = t[1]
            data[heading_1][heading_2] = {}
            heading_3 = None
        elif t[0] == 'heading_3':
            heading_3 = t[1]
            data[heading_1][heading_2][heading_3] = {}
        elif t[0] == 'field':
            field = t[1]
            value = None
        elif t[0] == 'value':
            value = t[1]

        if field and value:
            if heading_3:
                data[heading_1][heading_2][heading_3][field] = value
            elif heading_2:
                data[heading_1][heading_2][field] = value
            elif heading_1:
                data[heading_1][field] = value
            else:
                data[field] = value

    return result
