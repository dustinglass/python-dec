from requests import Session
from lxml.html import fromstring


EXIBIR_EM_ABAS = 'http://dec.fazenda.df.gov.br/autoUso.aspx?cmd=9&doc='
XPATHS = {
    'TituloAreaRestrita': '//span[@class="TituloAreaRestrita" and @style="background:#004800; color:#FFFFFF; font-weight:normal"]',
    'TextoFundoBrancoNegrito': '//span[@class="TextoFundoBrancoNegrito" and not(@style="visibility: hidden" or @style="visibility:hidden")]',
    'linha': '//span[@class="linha" and not(@style="visibility: hidden" or @style="visibility:hidden")]',
    'Detalhar': '//td[img[@title="Detalhar"]]'
}


class Nfce(object):
    
    def __init__(self, qr_code):
        
        self.qr_code = qr_code
        self.page = self._get_nfce()
        self.data = self._parse_nfce()
    
    def _get_nfce(self):
        
        session = Session()
        session.get(self.qr_code)
        return session.get(EXIBIR_EM_ABAS)

    def _parse_nfce(self):
        
        data = {None: {}}
        header = None
        num = None
        fields = []

        for i in fromstring(self.page.text).xpath('|'.join([i for i in XPATHS.values()])):
            # Parse text
            value = ''   
            try:
                value = _reduce_whitespace(i.xpath('./text()')[0])
            except:
                pass
            # Classify element
            try:
                class_ = i.xpath('./@class')[0]
            except:
                class_ = i.xpath('./img/@title')[0]
            # Process element
            if class_ == 'linha':
                if not num:
                    data[header][fields.pop(0)] = value
                else:
                    if not data['DADOS DOS PRODUTOS E SERVIÇOS'][num].get(header):
                        data['DADOS DOS PRODUTOS E SERVIÇOS'][num][header] = {}
                    data['DADOS DOS PRODUTOS E SERVIÇOS'][num][header][fields.pop(0)] = value
            elif class_ == 'TextoFundoBrancoNegrito':
                fields.append(value)
            elif class_ == 'TituloAreaRestrita':
                header = value
                data[header] = {}
                if header == 'TOTAIS':
                    num = None
            elif class_ == 'Detalhar':
                num = value
                header = None
                data['DADOS DOS PRODUTOS E SERVIÇOS'][num] = {header: {}}

        return data

    
def _reduce_whitespace(text):
    text = text.replace('\r', ' ').replace('\n', ' ')
    text = text.strip()
    while '  ' in text:
        text = text.replace('  ', ' ')
    return text
   
   
if __name__ == '__main__':

    nfce = Nfce('http://dec.fazenda.df.gov.br/ConsultarNFCe.aspx?chNFe=53180507738069000247651240000175261302020574&nVersao=100&tpAmb=1&cDest=33485616000159&dhEmi=323031382d30352d30335431303a33323a32302d30333a3030&vNF=96.49&vICMS=1.91&digVal=466b4676557730385432562b63325345646a5865475654565330553d&cIdToken=000001&cHashQRCode=2A198B90524BD91BA9B438D6D6E55071EB0C41EB')
    print(nfce.data)
