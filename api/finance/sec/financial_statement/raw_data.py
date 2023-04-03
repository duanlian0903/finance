import api.data.web.xml_parser as adwxp
import api.data.web.content as adwc
import api.finance.name.file.sec as afnfs
import api.common.data_type_operation.file as acdtof


def __get_quarterly_statement_link_list():
    url = 'https://www.sec.gov/dera/data/financial-statement-data-sets.html'
    urls = adwxp.get_all_the_urls_in_the_given_webpage(url)
    link_list = []
    for each_item in urls:
        if each_item.endswith('.zip'):
            link_list.append(adwxp.get_absolute_url(url, each_item))
    return link_list


def __save_given_zip_file(url):
    file_name = url.split('/')[-1]
    file_path = afnfs.get_sec_quarterly_financial_statement_folder()+'/'+file_name
    if not acdtof.check_file_existence(file_path):
        acdtof.save_binary_file(adwc.get_binary_content(url), file_path)


def download_all_quarterly_statement_zip_files():
    quarterly_statement_link_list = __get_quarterly_statement_link_list()
    for quarterly_statement_link in quarterly_statement_link_list:
        __save_given_zip_file(quarterly_statement_link)

