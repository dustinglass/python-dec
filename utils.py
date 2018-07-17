import re
from string import punctuation
import unicodedata


PUNCTUATION = re.compile('[%s]' % re.escape(punctuation))


def truncate_whitespace(text):
    """ Returns text with unnecessary whitespace removed. """
    text = text.replace('\r', ' ') \
               .replace('\n', ' ')
    text = text.strip()
    while '  ' in text:
        text = text.replace('  ', ' ')
    return text

def normalize(text):
    """ Return text as ASCII-normalized string. """
    return unicodedata.normalize('NFKD', text) \
                      .encode('ASCII', 'ignore') \
                      .decode('utf-8')

def standardize(text):
    """ Returns text in lowercase with punctuation
    and spaces replaced by underscores.
    """
    return truncate_whitespace(
            PUNCTUATION.sub(' ', text)
        ).replace(' ', '_').lower()
