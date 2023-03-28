import bs4
import api.data.web.xml.source_code as adwxsc


def get_soup_structure(html_source_code):
    return bs4.BeautifulSoup(html_source_code, 'html.parser')


def get_all_tags(soup_structure, tag_text):
    return soup_structure.find_all(tag_text)


def get_tag_attribute(tag, attribute_text):
    return tag.get(attribute_text)


def get_all_the_urls_in_the_given_webpage(given_webpage_url):
    html_source_code = adwxsc.get_xml_source_code(given_webpage_url)
    soup_structure = get_soup_structure(html_source_code)
    urls = []
    for tag in get_all_tags(soup_structure, 'a'):
        urls.append(get_tag_attribute(tag, 'href'))
    return urls
