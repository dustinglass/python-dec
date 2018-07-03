import re
from datetime import datetime
import json

UNITS = {
    'ml': ['ml'],
    'L': ['litro'],
    'g': ['g'],
    'kg': ['kg'],
    'un': ['unidades', 'unidade', 'un']
}
RE_UNITS = [
    re.compile('([0-9],)*([0-9]+)\s*([A-z]+)$'),
    re.compile('([0-9],)*([0-9]+)\s*([A-z]+)\s'),
    re.compile('([0-9],)*([0-9]+)\s*([A-z]+)\W')
]

class UnitString(object):

    def __init__(self, text):

        self.match = None
        self.value = None
        self.units = None

        text = text.lower()
        for r in RE_UNITS:
            match = re.search(r, text)
            if match:
                for k, v in UNITS.items():
                    for u in v:
                        if u == match.group(3):
                            self.match = match
                            self.units = k
                            if match.group(1):
                                self.value = float(
                                    match.group(1).replace(',', '') + '.' + \
                                    match.group(2)
                                )
                            else:
                                self.value = float(match.group(2))
                                return

def time_string():

    return datetime.utcnow().strftime('%Y%m%d%H%M%S%f')

def write_to_json(data, file_name):

    with open(file_name, 'w') as file:
        json.dump(data, file)

def read_from_json(file_name):

    with open(file_name, 'r') as file:
        return json.load(file)

def truncate_whitespace(text):

    text = text.replace('\r', ' ') \
               .replace('\n', ' ') \
               .replace('\t', ' ')
    text = text.strip()
    while '  ' in text:
        text = text.replace('  ', ' ')
    return text
