import requests


def get_xml_source_code(url):
    req = requests.get(url)
    return req.text
