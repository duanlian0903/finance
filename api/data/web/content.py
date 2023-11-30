import requests


def __get_requests_header():
    return {'User-Agent': 'Hofstra University lian.duan@hofstra.edu', 'Accept-Encoding': 'gzip, deflate', 'Host': 'www.sec.gov'}


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
