import bs4
import api.data.web.xml.source_code as adwxsc
import api.common.data_type_operation.check_data_type as acdtocdt


def get_soup_structure(html_source_code):
    try:
        return bs4.BeautifulSoup(html_source_code, 'html.parser')
    except:
        return None


def get_all_tags(soup_structure, tag_text):
    try:
        return soup_structure.find_all(tag_text)
    except:
        return []


def get_tag_attribute(tag, attribute_text):
    try:
        return tag.get(attribute_text)
    except:
        None


def get_all_the_urls_in_the_given_webpage(given_webpage_url):
    html_source_code = adwxsc.get_xml_source_code(given_webpage_url)
    soup_structure = get_soup_structure(html_source_code)
    urls = []
    for tag in get_all_tags(soup_structure, 'a'):
        href_attribute = get_tag_attribute(tag, 'href')
        if acdtocdt.whether_string(href_attribute):
            urls.append(href_attribute)
    return urls
