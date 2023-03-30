import api.finance.name.file.general as afnfg


def get_sec_folder():
    return afnfg.get_data_folder() + '/sec'


def get_sec_financial_statement_folder():
    return get_sec_folder() + '/financial_statement'

