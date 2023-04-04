import api.common.data_type_operation.file as acdtof
import api.common.data_type_operation.pandas as acdtop
import api.common.system.message as acsm
import api.finance.name.file.sec as afnfs
import api.finance.name.attribute.fundamental_analysis as afnafa
import api.finance.name.attribute.general as afnag


def __get_ticker_cik_dict():
    return acdtof.load_json_file_as_dict(afnfs.get_ticker_cik_json_file())


def __get_ticker_cik_df():
    ticker_cik_dict = __get_ticker_cik_dict()
    ticker_cik_df = acdtop.generate_multi_row_dataframe_from_list_or_nested_dictionary(ticker_cik_dict)
    ticker_cik_df = ticker_cik_df.T
    ticker_cik_df = acdtop.change_dataframe_column_name(ticker_cik_df, {'cik_str': afnafa.get_cik(), 'ticker': afnag.get_ticker(), 'title': afnag.get_company_name()})
    return ticker_cik_df


def __get_ticker_cik_df_with_ticker_index():
    return __get_ticker_cik_df().set_index(afnag.get_ticker())


def __get_ticker_cik_df_with_cik_index():
    return __get_ticker_cik_df().set_index(afnafa.get_cik())


def __get_quarterly_num_df(year, quarter):
    return acdtop.get_df_from_csv_file(afnfs.get_sec_quarterly_num_file(year, quarter), '\t')


def __get_quarterly_pre_df(year, quarter):
    return acdtop.get_df_from_csv_file(afnfs.get_sec_quarterly_pre_file(year, quarter), '\t')


def __get_quarterly_sub_df(year, quarter):
    return acdtop.get_df_from_csv_file(afnfs.get_sec_quarterly_sub_file(year, quarter), '\t')


def __get_quarterly_tag_df(year, quarter):
    return acdtop.get_df_from_csv_file(afnfs.get_sec_quarterly_tag_file(year, quarter), '\t')


def get_related_ticker(cik_num, ticker_cik_df_with_cik_index=__get_ticker_cik_df_with_cik_index()):
    try:
        ticker = ticker_cik_df_with_cik_index.loc[cik_num, afnag.get_ticker()]
        if not isinstance(ticker, str):
            ticker = list(ticker)[0]
        return ticker
    except:
        acsm.show_normal_operation_exception_message("Having error to get the related ticker for the given cik: " + str(cik_num))
        return None


def get_related_cik(ticker_str, ticker_cik_df_with_ticker_index=__get_ticker_cik_df_with_ticker_index()):
    try:
        cik = ticker_cik_df_with_ticker_index.loc[ticker_str, afnafa.get_cik()]
        return cik
    except:
        acsm.show_normal_operation_exception_message("Having error to get the related cik for the given ticker: " + str(ticker_str))
        return None


def get_existing_quarterly_report_list():
    folder_list = sorted(acdtof.get_folder_list(afnfs.get_sec_quarterly_financial_statement_folder()))
    existing_quarterly_report_list = []
    for folder in folder_list:
        existing_quarterly_report_list.append([int(folder[:4]), int(folder[-1])])
    return existing_quarterly_report_list
