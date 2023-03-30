import bs4
import api.data.web.content as adwc
import api.common.data_type_operation.check_data_type as acdtocdt
import api.common.data_type_operation.number_string_boolean_bytes as acdtonsbb


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


def get_absolute_url(given_webpage_url, relative_path):
    try:
        return given_webpage_url[:acdtonsbb.get_i_th_occurrence_position(3, given_webpage_url, '/')] + relative_path
    except:
        return None


def get_all_the_urls_in_the_given_webpage(given_webpage_url):
    html_source_code = adwc.get_source_text(given_webpage_url)
    soup_structure = get_soup_structure(html_source_code)
    urls = []
    for tag in get_all_tags(soup_structure, 'a'):
        href_attribute = get_tag_attribute(tag, 'href')
        if acdtocdt.whether_string(href_attribute):
            urls.append(href_attribute)
    return urls
