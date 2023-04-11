import api.common.data_type_operation.file as acdtof
import api.common.data_type_operation.dict as acdtod
import api.common.data_type_operation.pandas_numpy as acdtop
import api.common.data_type_operation.number_string_boolean_bytes as acdtonsbb
import api.common.data_type_operation.time as acdtot
import api.finance.name.file.sec as afnfs
import api.finance.name.attribute.fundamental_analysis as afnafa


def get_existing_cik_list():
    return sorted(acdtof.get_folder_list(afnfs.get_sec_cik_financial_statement_folder()))


def __get_tag_mapping_dict():
    return {
        afnafa.get_asset(): ['Asset', 'Assets'],
        afnafa.get_cash_and_cash_equivalent(): ['CashAndCashEquivalentsAtCarryingValue'],
        afnafa.get_total_liability(): ['Liabilities'],
        afnafa.get_short_term_liability(): ['LiabilitiesCurrent'],
        afnafa.get_long_term_liability(): ['LiabilitiesNoncurrent'],
        afnafa.get_equity(): ['StockholdersEquity'],
        afnafa.get_outstanding_share(): ['CommonStockSharesOutstanding'],
        afnafa.get_revenue(): ['RevenueFromContractWithCustomerExcludingAssessedTax', 'Revenue', 'Revenues'],
        afnafa.get_expense(): ['CostOfGoodsAndServicesSold', 'CostsAndExpenses'],
        afnafa.get_total_income(): ['OperatingIncomeLoss', 'GrossProfit'],
        afnafa.get_net_income(): ['NetIncomeLoss'],
        afnafa.get_eps(): ['BasicEarningsLossPerShare', 'EarningsPerShareBasic'],
        afnafa.get_diluted_eps(): ['DilutedEarningsLossPerShare', 'EarningsPerShareDiluted']
    }


def __generate_given_cik_unified_attribute_financial_statement(cik):
    original_json = acdtof.load_json_file_as_dict(afnfs.get_given_cik_original_financial_statement_summary_json_file(cik))
    modified_json = {}
    tag_mapping_dict = __get_tag_mapping_dict()
    for key in tag_mapping_dict:
        modified_json[key] = {}
        tag_list = tag_mapping_dict[key]
        for tag in tag_list:
            if tag in original_json:
                modified_json[key] = acdtod.merge_dict(modified_json[key], original_json[tag])
    acdtof.save_dict_as_json_file(modified_json, afnfs.get_given_cik_unified_attribute_financial_statement_summary_json_file(cik))


def __generate_all_unified_attribute_financial_statement():
    cik_list = get_existing_cik_list()
    for cik in cik_list:
        __generate_given_cik_unified_attribute_financial_statement(cik)


def __convert_date_string_into_datetime(date_string):
    year_str = date_string[:4]
    month_str = date_string[4:6]
    if int(month_str) <= 3:
        return acdtot.convert_string_to_datetime(year_str+'-03-30', acdtot.day_datetime_formatstring())
    elif int(month_str) <= 6:
        return acdtot.convert_string_to_datetime(year_str+'-06-30', acdtot.day_datetime_formatstring())
    elif int(month_str) <= 9:
        return acdtot.convert_string_to_datetime(year_str+'-09-30', acdtot.day_datetime_formatstring())
    else:
        return acdtot.convert_string_to_datetime(year_str+'-12-30', acdtot.day_datetime_formatstring())


def __get_non_time_interval_attribute_list():
    return [afnafa.get_asset(), afnafa.get_cash_and_cash_equivalent(), afnafa.get_total_liability(), afnafa.get_short_term_liability(), afnafa.get_long_term_liability(), afnafa.get_equity(), afnafa.get_outstanding_share()]


def __get_time_interval_attribute_list():
    return [afnafa.get_revenue(), afnafa.get_expense(), afnafa.get_total_income(), afnafa.get_net_income(), afnafa.get_eps(), afnafa.get_diluted_eps()]


def __get_raw_financial_statement_df(unified_cik_dict):
    converted_dict = {}
    non_time_interval_attribute_list = __get_non_time_interval_attribute_list()
    time_interval_attribute_list = __get_time_interval_attribute_list()
    for current_attribute in non_time_interval_attribute_list + time_interval_attribute_list:
        detail_data = unified_cik_dict[current_attribute]
        for date_string in detail_data:
            current_date = __convert_date_string_into_datetime(date_string)
            if current_date in converted_dict:
                if current_attribute in non_time_interval_attribute_list:
                    converted_dict[current_date][current_attribute] = detail_data[date_string]['0']['value']
                else:
                    for duration in '1234':
                        if duration in detail_data[date_string]:
                            converted_dict[current_date][current_attribute+' Q'+duration] = detail_data[date_string][duration]['value']
                        else:
                            converted_dict[current_date][current_attribute+' Q'+duration] = acdtonsbb.get_nan_value()
            else:
                if current_attribute in non_time_interval_attribute_list:
                    converted_dict[current_date] = {current_attribute: detail_data[date_string]['0']['value']}
                else:
                    converted_dict[current_date] = {}
                    for duration in '1234':
                        if duration in detail_data[date_string]:
                            converted_dict[current_date][current_attribute+' Q'+duration] = detail_data[date_string][duration]['value']
                        else:
                            converted_dict[current_date][current_attribute+' Q'+duration] = acdtonsbb.get_nan_value()
    return acdtop.generate_multi_row_dataframe_from_nested_dictionary(converted_dict).sort_index()


def __get_aligned_index_financial_statement_df(raw_financial_statement_df):
    if len(raw_financial_statement_df) > 0:
        start_index = raw_financial_statement_df.index[0]
        end_index = raw_financial_statement_df.index[-1]
        aligned_index_list = [start_index]
        current_index = start_index
        while current_index < end_index:
            current_index = acdtot.get_needed_datetime_with_month_interval(current_index, 3)
            aligned_index_list.append(current_index)
        align_df = acdtop.generate_multi_row_dataframe_from_matrix([[0]]*len(aligned_index_list), ['Align'])
        align_df.index = aligned_index_list
        return acdtop.join_auxiliary_df(align_df, raw_financial_statement_df).iloc[:, 1:]
    else:
        return acdtop.get_empty_data_frame()


def __get_q1_filled_financial_statement_df(aligned_index_financial_statement_df):
    q1_filled_financial_statement_df = aligned_index_financial_statement_df.copy()
    time_interval_attribute_list = __get_time_interval_attribute_list()
    for current_attribute in time_interval_attribute_list:
        if current_attribute + ' Q1' in aligned_index_financial_statement_df.columns:
            for index_num in range(len(aligned_index_financial_statement_df)):
                # if empty in the beginning, try use q2, q3 or q4 to calculate
                if acdtonsbb.whether_nan_value(q1_filled_financial_statement_df.loc[q1_filled_financial_statement_df.index[index_num], current_attribute + ' Q1']):
                    if not acdtonsbb.whether_nan_value(q1_filled_financial_statement_df.loc[q1_filled_financial_statement_df.index[index_num], current_attribute + ' Q2']):
                        if index_num >= 1:
                            q1_filled_financial_statement_df.loc[q1_filled_financial_statement_df.index[index_num], current_attribute + ' Q1'] = q1_filled_financial_statement_df.loc[q1_filled_financial_statement_df.index[index_num], current_attribute + ' Q2'] - q1_filled_financial_statement_df.loc[q1_filled_financial_statement_df.index[index_num-1], current_attribute + ' Q1']
                    elif not acdtonsbb.whether_nan_value(q1_filled_financial_statement_df.loc[q1_filled_financial_statement_df.index[index_num], current_attribute + ' Q3']):
                        if index_num >= 2:
                            q1_filled_financial_statement_df.loc[q1_filled_financial_statement_df.index[index_num], current_attribute + ' Q1'] = q1_filled_financial_statement_df.loc[q1_filled_financial_statement_df.index[index_num], current_attribute + ' Q3'] - q1_filled_financial_statement_df.loc[q1_filled_financial_statement_df.index[index_num-1], current_attribute + ' Q1'] - q1_filled_financial_statement_df.loc[q1_filled_financial_statement_df.index[index_num-2], current_attribute + ' Q1']
                    elif not acdtonsbb.whether_nan_value(q1_filled_financial_statement_df.loc[q1_filled_financial_statement_df.index[index_num], current_attribute + ' Q4']):
                        if index_num >= 3:
                            q1_filled_financial_statement_df.loc[q1_filled_financial_statement_df.index[index_num], current_attribute + ' Q1'] = q1_filled_financial_statement_df.loc[q1_filled_financial_statement_df.index[index_num], current_attribute + ' Q4'] - q1_filled_financial_statement_df.loc[q1_filled_financial_statement_df.index[index_num-1], current_attribute + ' Q1'] - q1_filled_financial_statement_df.loc[q1_filled_financial_statement_df.index[index_num-2], current_attribute + ' Q1'] - q1_filled_financial_statement_df.loc[q1_filled_financial_statement_df.index[index_num-3], current_attribute + ' Q1']
                # if still empty after the calculation, try to use q2, q3, or q4 average to fill
                if acdtonsbb.whether_nan_value(q1_filled_financial_statement_df.loc[q1_filled_financial_statement_df.index[index_num], current_attribute + ' Q1']):
                    for trial_index_num in range(index_num, min(index_num+2, len(aligned_index_financial_statement_df))):
                        if not acdtonsbb.whether_nan_value(q1_filled_financial_statement_df.loc[q1_filled_financial_statement_df.index[trial_index_num], current_attribute + ' Q2']):
                            q1_filled_financial_statement_df.loc[q1_filled_financial_statement_df.index[index_num], current_attribute + ' Q1'] = q1_filled_financial_statement_df.loc[q1_filled_financial_statement_df.index[trial_index_num], current_attribute + ' Q2']/2
                if acdtonsbb.whether_nan_value(q1_filled_financial_statement_df.loc[q1_filled_financial_statement_df.index[index_num], current_attribute + ' Q1']):
                    for trial_index_num in range(index_num, min(index_num+3, len(aligned_index_financial_statement_df))):
                        if not acdtonsbb.whether_nan_value(q1_filled_financial_statement_df.loc[q1_filled_financial_statement_df.index[trial_index_num], current_attribute + ' Q3']):
                            q1_filled_financial_statement_df.loc[q1_filled_financial_statement_df.index[index_num], current_attribute + ' Q1'] = q1_filled_financial_statement_df.loc[q1_filled_financial_statement_df.index[trial_index_num], current_attribute + ' Q3']/3
                if acdtonsbb.whether_nan_value(q1_filled_financial_statement_df.loc[q1_filled_financial_statement_df.index[index_num], current_attribute + ' Q1']):
                    for trial_index_num in range(index_num, min(index_num+4, len(aligned_index_financial_statement_df))):
                        if not acdtonsbb.whether_nan_value(q1_filled_financial_statement_df.loc[q1_filled_financial_statement_df.index[trial_index_num], current_attribute + ' Q4']):
                            q1_filled_financial_statement_df.loc[q1_filled_financial_statement_df.index[index_num], current_attribute + ' Q1'] = q1_filled_financial_statement_df.loc[q1_filled_financial_statement_df.index[trial_index_num], current_attribute + ' Q4']/4
    return q1_filled_financial_statement_df


def __get_cleaned_financial_statement_df(q1_filled_financial_statement_df):
    time_interval_attribute_list = __get_time_interval_attribute_list()
    non_time_interval_attribute_list = __get_non_time_interval_attribute_list()
    for non_time_interval_attribute in non_time_interval_attribute_list:
        if non_time_interval_attribute not in q1_filled_financial_statement_df.columns:
            q1_filled_financial_statement_df[non_time_interval_attribute] = acdtonsbb.get_nan_value()
    for time_interval_attribute in time_interval_attribute_list:
        if time_interval_attribute + ' Q1' not in q1_filled_financial_statement_df.columns:
            q1_filled_financial_statement_df[time_interval_attribute + ' Q1'] = acdtonsbb.get_nan_value()
    cleaned_financial_statement_df = q1_filled_financial_statement_df[non_time_interval_attribute_list]
    rename_dict = {}
    selected_attribute_list = []
    for time_interval_attribute in time_interval_attribute_list:
        rename_dict[time_interval_attribute + ' Q1'] = time_interval_attribute
        selected_attribute_list.append(time_interval_attribute + ' Q1')
    cleaned_financial_statement_df = acdtop.combine_dataframe([cleaned_financial_statement_df, acdtop.change_dataframe_column_name(q1_filled_financial_statement_df[selected_attribute_list], rename_dict)], axis=1)
    return cleaned_financial_statement_df[non_time_interval_attribute_list + time_interval_attribute_list]


def __generate_given_cik_cleaned_attribute_financial_statement_df(cik):
    unified_cik_dict = acdtof.load_json_file_as_dict(afnfs.get_given_cik_unified_attribute_financial_statement_summary_json_file(cik))
    raw_financial_statement_df = __get_raw_financial_statement_df(unified_cik_dict)
    aligned_index_financial_statement_df = __get_aligned_index_financial_statement_df(raw_financial_statement_df)
    q1_filled_financial_statement_df = __get_q1_filled_financial_statement_df(aligned_index_financial_statement_df)
    cleaned_financial_statement_df = __get_cleaned_financial_statement_df(q1_filled_financial_statement_df)
    acdtof.save_pickle_data(cleaned_financial_statement_df, afnfs.get_given_cik_financial_statement_df_file(cik), True)


def __generate_all_cleaned_attribute_financial_statement_df():
    cik_list = get_existing_cik_list()
    for cik in cik_list:
        __generate_given_cik_cleaned_attribute_financial_statement_df(cik)


def generate_all_modified_financial_statement_df():
    __generate_all_unified_attribute_financial_statement()
    __generate_all_cleaned_attribute_financial_statement_df()
