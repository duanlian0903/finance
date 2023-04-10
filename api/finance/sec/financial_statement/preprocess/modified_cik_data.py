import api.common.data_type_operation.file as acdtof
import api.common.data_type_operation.dict as acdtod
import api.common.data_type_operation.pandas as acdtop
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


def generate_all_unified_attribute_financial_statement():
    cik_list = get_existing_cik_list()
    for cik in cik_list:
        __generate_given_cik_unified_attribute_financial_statement(cik)


def __convert_date_string_into_datetime(date_string):
    year_str = date_string[:4]
    month_str = date_string[4:6]
    if int(month_str) <= 3:
        return acdtot.convert_string_to_datetime(year_str+'-03-31', acdtot.day_datetime_formatstring())
    elif int(month_str) <= 6:
        return acdtot.convert_string_to_datetime(year_str+'-06-30', acdtot.day_datetime_formatstring())
    elif int(month_str) <= 9:
        return acdtot.convert_string_to_datetime(year_str+'-09-30', acdtot.day_datetime_formatstring())
    else:
        return acdtot.convert_string_to_datetime(year_str+'-12-31', acdtot.day_datetime_formatstring())


def __get_non_time_interval_attribute_list():
    return [afnafa.get_asset(), afnafa.get_cash_and_cash_equivalent(), afnafa.get_total_liability(), afnafa.get_short_term_liability(), afnafa.get_long_term_liability(), afnafa.get_equity(), afnafa.get_outstanding_share()]


def __get_time_interval_attribute_list():
    return [afnafa.get_revenue(), afnafa.get_expense(), afnafa.get_total_income(), afnafa.get_net_income(), afnafa.get_eps(), afnafa.get_diluted_eps()]


def __generate_non_time_interval_attribute_df(unified_cik_dict):
    non_time_interval_attribute_list = __get_non_time_interval_attribute_list()
    converted_dict = {}
    for non_time_interval_attribute in non_time_interval_attribute_list:
        detail_data = unified_cik_dict[non_time_interval_attribute]
        for date_string in detail_data:
            current_date = __convert_date_string_into_datetime(date_string)
            if current_date in converted_dict:
                converted_dict[current_date][non_time_interval_attribute] = detail_data[date_string]['0']['value']
            else:
                converted_dict[current_date] = {non_time_interval_attribute: detail_data[date_string]['0']['value']}
    non_time_interval_attribute_df = acdtop.generate_multi_row_dataframe_from_list_of_dictionary(converted_dict)
    check = 1


def __generate_given_cik_cleaned_attribute_financial_statement_df(cik):
    unified_cik_dict = acdtof.load_json_file_as_dict(afnfs.get_given_cik_unified_attribute_financial_statement_summary_json_file(cik))
    __generate_non_time_interval_attribute_df(unified_cik_dict)
    check = 1


def generate_all_cleaned_attribute_financial_statement_df():
    cik_list = get_existing_cik_list()
    for cik in cik_list:
        __generate_given_cik_cleaned_attribute_financial_statement_df(cik)
