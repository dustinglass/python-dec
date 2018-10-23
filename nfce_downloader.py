import re
import requests
from lxml.html import fromstring
import os
import subprocess
from pdf2image import convert_from_path


QR_CODE = 'http://dec.fazenda.df.gov.br/ConsultarNFCe.aspx?chNFe=53180507738069000247651240000175261302020574&nVersao=100&tpAmb=1&cDest=33485616000159&dhEmi=323031382d30352d30335431303a33323a32302d30333a3030&vNF=96.49&vICMS=1.91&digVal=466b4676557730385432562b63325345646a5865475654565330553d&cIdToken=000001&cHashQRCode=2A198B90524BD91BA9B438D6D6E55071EB0C41EB'


def download_nfce(qr_code):
    chave_de_acesso, valor = _parse_qr_code(qr_code)
    data_de_emissao = _parse_html(fromstring(requests.get(qr_code).text))
    _download_images(qr_code, _build_file_name(data_de_emissao, 
                                               valor, 
                                               chave_de_acesso))

def _parse_qr_code(qr_code):
    # Parses desired values from QR code
    chave_de_acesso = re.search('chNFe=(\d{44})', qr_code).group(1)
    valor = 'R${}'.format(re.search('vNF=(\d+.\d+)', qr_code).group(1)
                  .replace('.', ','))
    return chave_de_acesso, valor

def _parse_html(html):
    # Parses desired values from NFCE page
    div = html.xpath('//div[@id="divNFCeOnline"]')[0]
    data_de_emissao = _parse_data_de_emissao(div)
    return data_de_emissao

def _parse_data_de_emissao(element):
    # Parses receipt printed date
    data_de_emissao = element.xpath('.//td[@class="NFCCabecalho_SubTitulo" '
                                    'and contains(text(), "Data de Emissão:")]'
                                    '/text()')[0]
    data_de_emissao = re.search('Data de Emissão:\s+(\d{2}/\d{2}/\d{4})',
                                data_de_emissao).group(1)
    return '{}.{}.{}'.format(data_de_emissao[6:10], 
                             data_de_emissao[3:5], 
                             data_de_emissao[0:2])

def _build_file_name(data_de_emissao, valor, chave_de_acesso):
    # Creates a informative and unique file name for the receipt
    return '{}_{}_{}'.format(data_de_emissao, valor, chave_de_acesso)

def _download_images(qr_code, file_name):
    # Download webpage as 200 dpi image(s)
    pdf_path = '{}.pdf'.format(file_name)
    subprocess.run(['wkhtmltopdf', '--lowquality', qr_code, pdf_path])
    os.mkdir(file_name)
    convert_from_path(pdf_path, output_folder=file_name)
    os.remove(pdf_path)


if __name__ == '__main__':
    download_nfce(QR_CODE)