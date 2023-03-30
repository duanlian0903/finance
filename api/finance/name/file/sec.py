import api.finance.name.file.general as afnfg


def get_sec_folder():
    return afnfg.get_data_folder() + '/sec'


def get_sec_financial_statement_folder():
    return get_sec_folder() + '/financial_statement'


def get_sec_quarterly_financial_statement_zip_file(year, quarter):
    return get_sec_financial_statement_folder() + '/' + str(year) + 'q' + str(quarter) + '.zip'
