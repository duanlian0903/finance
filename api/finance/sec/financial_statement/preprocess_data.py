import api.common.data_type_operation.file as acdtof
import api.common.data_type_operation.pandas as acdtop
import api.common.data_type_operation.dict as acdtod
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


def __update_quarterly_summary_dict(year, quarter):
    if acdtof.check_file_existence(afnfs.get_given_sec_quarterly_financial_statement_summary_json_file(year, quarter)):
        acsm.show_normal_operation_exception_message('Skip the update because the summary for this quarter exists with (' + str(year) + ', ' + str(quarter) + ')')
    else:
        num_df = __get_quarterly_num_df(year, quarter)
        sub_df = __get_quarterly_sub_df(year, quarter)
        summary_dict = {}
        cik_set = set(sub_df['cik'])
        for cik in cik_set:
            related_sub_df = sub_df[sub_df['cik'] == cik].sort_values(['accepted'])
            for index_i in related_sub_df.index:
                adsh = related_sub_df.loc[index_i, 'adsh']
                related_num_df = num_df[num_df['adsh'] == adsh]
                for index_j in related_num_df.index:
                    tag = related_num_df.loc[index_j, 'tag']
                    ddate = str(related_num_df.loc[index_j, 'ddate'])
                    qtrs = str(related_num_df.loc[index_j, 'qtrs'])
                    uom = related_num_df.loc[index_j, 'uom']
                    value = related_num_df.loc[index_j, 'value']
                    if str(cik) not in summary_dict:
                        summary_dict[str(cik)] = {}
                    if tag not in summary_dict[str(cik)]:
                        summary_dict[str(cik)][tag] = {}
                    if ddate not in summary_dict[str(cik)][tag]:
                        summary_dict[str(cik)][tag][ddate] = {}
                    summary_dict[str(cik)][tag][ddate][qtrs] = {'value': value, 'unit': uom}
        acdtof.save_dict_as_json_file(summary_dict, afnfs.get_given_sec_quarterly_financial_statement_summary_json_file(year, quarter))


def __get_quarterly_summary_dict(year, quarter):
    return acdtof.load_json_file_as_dict(afnfs.get_given_sec_quarterly_financial_statement_summary_json_file(year, quarter))


def __update_all_quarterly_summary_dict():
    existing_quarterly_report_list = get_existing_quarterly_report_list()
    for quarterly_para in existing_quarterly_report_list:
        acsm.show_normal_operation_progress_message('Start processing quarterly summary dict for ' + str(quarterly_para))
        __update_quarterly_summary_dict(quarterly_para[0], quarterly_para[1])


def __update_all_cik_summary_dict():
    existing_quarterly_report_list = get_existing_quarterly_report_list()
    for quarterly_para in existing_quarterly_report_list:
        acsm.show_normal_operation_progress_message('Start processing cik summary dict with ' + str(quarterly_para))
        quarterly_summary_dict = __get_quarterly_summary_dict(quarterly_para[0], quarterly_para[1])
        for cik in quarterly_summary_dict:
            existing_information_dict = acdtof.load_json_file_as_dict(afnfs.get_given_cik_financial_statement_summary_json_file(cik))
            current_information_dict = quarterly_summary_dict[cik]
            updated_information_dict = acdtod.merge_dict(existing_information_dict, current_information_dict)
            acdtof.save_dict_as_json_file(updated_information_dict, afnfs.get_given_cik_financial_statement_summary_json_file(cik))


def preprocess_data():
    __update_all_quarterly_summary_dict()
    __update_all_cik_summary_dict()
