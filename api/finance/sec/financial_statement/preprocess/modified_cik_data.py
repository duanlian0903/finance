import api.common.data_type_operation.file as acdtof
import api.finance.name.file.sec as afnfs


def get_existing_cik_list():
    return sorted(acdtof.get_folder_list(afnfs.get_sec_cik_financial_statement_folder()))
