import requests


def __get_requests_header():
    return {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}


def get_xml_source_code(url, headers=__get_requests_header(), timeout=10):
    try:
        req = requests.get(url, headers=headers, timeout=timeout)
        return req.text
    except:
        return None

