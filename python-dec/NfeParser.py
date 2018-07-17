#!/usr/bin/python3
# -*- coding: utf-8 -*- 


from utils import *
from bs4 import BeautifulSoup


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


class NfeParser:

    def __init__(self, html):

        self.data = tuples_to_dict(html_to_tuples(html))

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
