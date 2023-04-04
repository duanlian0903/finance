import api.common.data_type_operation.file as acdtof
import api.common.data_type_operation.pandas as acdtop
import api.finance.name.file.sec as afnfs
import api.finance.name.attribute.fundamental_analysis as afnafa


def __get_ticker_cik_dict():
    return acdtof.load_json_file_as_dict(afnfs.get_ticker_cik_json_file())


def __get_ticker_cik_df():
    ticker_cik_dict = __get_ticker_cik_dict()
    ticker_cik_df = acdtop.generate_multi_row_dataframe_from_list_or_nested_dictionary(ticker_cik_dict)
    ticker_cik_df = ticker_cik_df.T.set_index('ticker')
    ticker_cik_df = acdtop.change_dataframe_column_name(ticker_cik_df, {'cik_str': afnafa.get_cik(), 'title': afnafa.get_company_name()})
    return ticker_cik_df
