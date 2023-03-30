import api.data.web.xml.parser as adwxp


def get_quarterly_statement_link_list():
    url = 'https://www.sec.gov/dera/data/financial-statement-data-sets.html'
    urls = adwxp.get_all_the_urls_in_the_given_webpage(url)
    link_list = []
    for each_item in urls:
        if each_item.endswith('.zip'):
            link_list.append(adwxp.get_absolute_url(url, each_item))
    return link_list