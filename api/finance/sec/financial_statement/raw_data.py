import api.data.web.xml_parser as adwxp
import api.data.web.content as adwc
import api.finance.name.file.sec as afnfs
import api.common.data_type_operation.file as acdtof
import api.common.data_type_operation.number_string_boolean_bytes as acdtonsbb


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
        acdtof.save_file(adwc.get_binary_content(url), file_path)


def __download_all_quarterly_statement_zip_files():
    quarterly_statement_link_list = __get_quarterly_statement_link_list()
    for quarterly_statement_link in quarterly_statement_link_list:
        __save_given_zip_file(quarterly_statement_link)


def __unzip_all_quarterly_statement_zip_files():
    file_list = acdtof.get_file_list(afnfs.get_sec_quarterly_financial_statement_folder())
    for file in file_list:
        if file.endswith('.zip'):
            related_folder = afnfs.get_sec_quarterly_financial_statement_folder()+'/'+file[:-4]
            if not acdtof.check_folder_existence(related_folder):
                acdtof.unzip_zip_file(afnfs.get_sec_quarterly_financial_statement_folder()+'/'+file, related_folder)


def __update_sec_ticker_cik_json_file():
    url = 'https://www.sec.gov/files/company_tickers.json'
    acdtof.save_file(acdtonsbb.get_string_from_bytes_with_utf_8(adwc.get_binary_content(url)), afnfs.get_ticker_cik_json_file(), False)


def prepare_sec_raw_data():
    __download_all_quarterly_statement_zip_files()
    __unzip_all_quarterly_statement_zip_files()
    __update_sec_ticker_cik_json_file()
