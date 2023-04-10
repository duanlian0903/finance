import api.common.data_type_operation.file as acdtof
import api.common.data_type_operation.dict as acdtod
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
        afnafa.get_revenue(): ['RevenueFromContractWithCustomerExcludingAssessedTax', 'Revenue', 'Revenues'],
        afnafa.get_expense(): ['CostOfGoodsAndServicesSold', 'CostsAndExpenses'],
        afnafa.get_total_income(): ['OperatingIncomeLoss', 'GrossProfit'],
        afnafa.get_net_income(): ['NetIncomeLoss'],
        afnafa.get_outstanding_share(): ['CommonStockSharesOutstanding'],
        afnafa.get_eps(): ['BasicEarningsLossPerShare', 'EarningsPerShareBasic'],
        afnafa.get_diluted_eps(): ['DilutedEarningsLossPerShare', 'EarningsPerShareDiluted']
    }


def __generate_given_cik_modified_financial_statement(cik):
    original_json = acdtof.load_json_file_as_dict(afnfs.get_given_cik_original_financial_statement_summary_json_file(cik))
    modified_json = {}
    tag_mapping_dict = __get_tag_mapping_dict()
    for key in tag_mapping_dict:
        modified_json[key] = {}
        tag_list = tag_mapping_dict[key]
        for tag in tag_list:
            if tag in original_json:
                modified_json[key] = acdtod.merge_dict(modified_json[key], original_json[tag])
    acdtof.save_dict_as_json_file(modified_json, afnfs.get_given_cik_modified_financial_statement_summary_json_file(cik))


def generate_all_modified_financial_statement():
    cik_list = get_existing_cik_list()
    for cik in cik_list:
        __generate_given_cik_modified_financial_statement(cik)
