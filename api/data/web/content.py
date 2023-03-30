import requests


def __get_requests_header():
    return {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}


def get_request(url, headers=__get_requests_header(), timeout=10):
    try:
        return requests.get(url, headers=headers, timeout=timeout)
    except:
        return None


def get_binary_content(url, headers=__get_requests_header(), timeout=10):
    try:
        return get_request(url, headers=headers, timeout=timeout).content
    except:
        return None


def get_source_text(url, headers=__get_requests_header(), timeout=10):
    try:
        return get_request(url, headers=headers, timeout=timeout).text
    except:
        return None

