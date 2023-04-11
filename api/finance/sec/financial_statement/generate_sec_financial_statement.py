import api.finance.sec.financial_statement.raw_data as afsfsrd
import api.finance.sec.financial_statement.preprocess.original_cik_data as afsfspocd
import api.finance.sec.financial_statement.preprocess.modified_cik_data as afsfspmcd
import api.finance.name.file.sec as afnfs
import api.common.data_type_operation.file as acdtof


def generate_sec_financial_statement():
    afsfsrd.prepare_sec_raw_data()
    afsfspocd.get_original_cik_data()
    afsfspmcd.generate_all_modified_financial_statement_df()


def get_financial_statement(ticker):
    cik = afsfspocd.get_related_cik(ticker, afsfspocd.__get_ticker_cik_df_with_ticker_index())
    return acdtof.load_pickle_data(afnfs.get_given_cik_financial_statement_df_file(cik))
