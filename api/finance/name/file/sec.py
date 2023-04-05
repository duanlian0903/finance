import api.finance.name.file.general as afnfg


def get_sec_folder():
    return afnfg.get_data_folder() + '/sec'


def get_sec_financial_statement_folder():
    return get_sec_folder() + '/financial_statement'


def get_sec_quarterly_financial_statement_folder():
    return get_sec_financial_statement_folder() + '/quarter'


def get_sec_quarterly_financial_statement_zip_file(year, quarter):
    return get_sec_quarterly_financial_statement_folder() + '/' + str(year) + 'q' + str(quarter) + '.zip'


def get_given_sec_quarterly_financial_statement_folder(year, quarter):
    return get_sec_quarterly_financial_statement_folder() + '/' + str(year) + 'q' + str(quarter)


def get_sec_quarterly_num_file(year, quarter):
    return get_given_sec_quarterly_financial_statement_folder(year, quarter) + '/num.txt'


def get_sec_quarterly_pre_file(year, quarter):
    return get_given_sec_quarterly_financial_statement_folder(year, quarter) + '/pre.txt'


def get_sec_quarterly_sub_file(year, quarter):
    return get_given_sec_quarterly_financial_statement_folder(year, quarter) + '/sub.txt'


def get_sec_quarterly_tag_file(year, quarter):
    return get_given_sec_quarterly_financial_statement_folder(year, quarter) + '/tag.txt'


def get_given_sec_quarterly_financial_statement_summary_json_file(year, quarter):
    return get_given_sec_quarterly_financial_statement_folder(year, quarter) + '/summary.json'


def get_sec_cik_financial_statement_folder():
    return get_sec_financial_statement_folder() + '/cik'


def get_given_cik_financial_statement_summary_json_file(cik):
    return get_sec_cik_financial_statement_folder() + '/' + str(cik) + '.json'


def get_ticker_cik_json_file():
    return get_sec_folder() + '/company_tickers.json'
